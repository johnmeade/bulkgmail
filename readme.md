
Install
---

Requires python 3.6+

```
python3.6 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


Usage
---

* Obtain a `credentials.json` file from the [gmail API quickstart](https://developers.google.com/gmail/api/quickstart/python) by clicking the "Enable the GMail API" button, and place it in the root of the project.

* Create "body.txt" and "subject.txt" files in the "templates" folder. These files define the body and subject of the emails that will be sent, and they will be rendered with the Jinja templating engine. Example body:

        Hi {{name}}, what's up?

* Create a CSV file containing all the data for your template. Each row is an individual email that will be sent. There must be an "email" field in the CSV, which is where the email will be sent. Example:

        email,name
        bill@gmail.com,Bill

* Run like so:

        python -m bulkgmail --sender you@gmail.com --data data.csv

For an example of building a mass email campaign, where each email has a unique code and a URL, see the "exmaples" folder.
