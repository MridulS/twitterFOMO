# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pandas as pd

from datetime import datetime, timedelta

email_date = str((datetime.today() - timedelta(days=1)).date())
filename = "data/" + "tweets_" + email_date + ".pickle"
data = pd.read_pickle(filename)

content = list()
for tweet in data.itertuples():
    text = tweet.full_text
    user = tweet.user["name"]
    link = "https://twitter.com/i/web/status/" + str(tweet.id)
    content.append(str("<li>" + text + " - " + user + " - " + link + "</li>"))

content = " \n ".join(content)

message = Mail(
    from_email=os.environ.get("FROM_EMAIL"),
    to_emails=os.environ.get("TO_EMAIL"),
    subject="Twitter Update for" + email_date,
    html_content="<ul>" + content + "</ul>",
)
try:
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
