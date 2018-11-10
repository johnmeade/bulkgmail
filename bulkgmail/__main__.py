import csv
from os.path import join, exists
from argparse import ArgumentParser
from time import sleep
from .util import HERE, FP_TEMPLATES
from .gmail import send

#
#  Init
#

FP_BODY = join(FP_TEMPLATES, 'body.txt')
FP_SUBJECT = join(FP_TEMPLATES, 'subject.txt')

if not exists(FP_BODY):
    raise(Exception(f'please make a "body.txt" file in the "{FP_TEMPLATES}"" folder'))

if not exists(FP_SUBJECT):
    raise(Exception(f'please make a "subject.txt" file in the "{FP_TEMPLATES}"" folder'))

with open(FP_BODY, 'r') as f:
    BODY_TMP = f.read()

with open(FP_SUBJECT, 'r') as f:
    SUBJECT_TMP = f.read()

#
#  Main
#

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--data", required=True, type=str,
        help='CSV file defining variables to be injected into the Jinja templates')
    parser.add_argument("--sender", required=True, type=str,
        help='Sender email address (this should match the Google account that generated the "credentials.json" file)')
    args = parser.parse_args()

    codes = set()

    with open(args.data, 'r') as f:
        contexts = list(csv.DictReader(f))

    for context in contexts:
        # send email and sleep to stay under usage limits
        send(sender=args.sender, to=context['email'], context=context)
        sleep(0.5)
