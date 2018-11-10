'''
Send email through gmail, with Jinja templating support.
'''

import sys
import base64
from os.path import join, exists
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from jinja2 import Environment, FileSystemLoader

from .util import FP_TEMPLATES

#
#  Filepaths
#

FP_BODY = join(FP_TEMPLATES, 'body.txt')
FP_SUBJECT = join(FP_TEMPLATES, 'subject.txt')

if not exists(FP_BODY):
    raise(Exception(f'please make a "body.txt" file in the "{FP_TEMPLATES}"" folder'))

if not exists(FP_SUBJECT):
    raise(Exception(f'please make a "subject.txt" file in the "{FP_TEMPLATES}"" folder'))

#
#  Init
#

JENV = Environment(loader=FileSystemLoader(FP_TEMPLATES))

# NOTE: If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.send'


def service():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        sys.argv = [sys.argv[0]] # ugh
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('gmail', 'v1', http=creds.authorize(Http()))


def send(sender, to, context):
    # render templates
    body_tmpl = JENV.get_template('body.txt')
    body = body_tmpl.render(context)
    subject_tmpl = JENV.get_template('subject.txt')
    subject = subject_tmpl.render(context)
    # build mime email message
    mime_msg = MIMEText(body)
    mime_msg['to'] = to
    mime_msg['from'] = sender
    mime_msg['subject'] = subject
    raw_msg = { 'raw': base64.urlsafe_b64encode(mime_msg.as_bytes()).decode() }
    # Call the Gmail API
    try:
        sent_msg = service().users().messages().send(userId='me', body=raw_msg).execute()
        print(f'Message id {sent_msg["id"]} successfully sent to "{to}"')
        return sent_msg
    except Exception as error:
        print(f'Error when sending to "{to}":\n{error}\n')
