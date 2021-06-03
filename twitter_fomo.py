import ast
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import schedule
import tweepy
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logging.basicConfig(
    filename="logs.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


def get_twitter_timeline(
    consumer_key, consumer_secret, access_token, access_token_secret
):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    logging.debug("Fetching home timeline.")
    public_tweets = api.home_timeline(count=200, tweet_mode="extended")

    df = pd.DataFrame.from_records([tweet._json for tweet in public_tweets])
    df.created_at = pd.to_datetime(df.created_at)
    df["date"] = df.created_at.apply(lambda x: x.date())
    df = df[["id", "user", "full_text", "date"]]
    dates = df.date.unique()

    for i in dates:
        my_file = Path("data/" + "tweets_" + str(i) + ".csv")
        if my_file.is_file():
            temp_read = pd.read_csv(my_file)
            new_dump = pd.concat([temp_read, df[df.date == i]]).drop_duplicates(
                subset="id"
            )
            new_dump.to_csv(my_file, index=False)
        else:
            logging.debug(f"Creating file {my_file}")
            df[df.date == i].to_csv(my_file, index=False)


def send_email(SENDGRID_API_KEY, from_email, to_emails):
    email_date = str((datetime.today() - timedelta(days=1)).date())
    filename = "data/" + "tweets_" + email_date + ".csv"
    data = pd.read_csv(filename)

    logging.debug(f"Creating content for {email_date}")
    content = list()
    for tweet in data.itertuples():
        text = tweet.full_text
        user = ast.literal_eval(tweet.user)["name"]
        link = "https://twitter.com/i/web/status/" + str(tweet.id)
        content.append(str("<li>" + text + " - " + user + " - " + link + "</li>"))

    content = " \n ".join(content)

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject="Twitter Update for " + email_date,
        html_content="<ul>" + content + "</ul>",
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.debug(response.status_code)
        logging.debug(response.body)
        logging.debug(response.headers)
    except Exception as e:
        logging.debug(e.message)


if __name__ == "__main__":
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    access_token = os.environ.get("TWITTER_TOKEN")
    access_token_secret = os.environ.get("TWITTER_TOKEN_SECRET")
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
    from_email = os.environ.get("FROM_EMAIL")
    to_emails = os.environ.get("TO_EMAIL")
    fetch = os.environ.get("FETCH")
    # get_twitter_timeline(consumer_key, consumer_secret, access_token, access_token_secret)
    # send_email(SENDGRID_API_KEY, from_email, to_emails)
    def _fetch_tweet_job():
        get_twitter_timeline(
            consumer_key, consumer_secret, access_token, access_token_secret
        )

    def _send_email():
        send_email(SENDGRID_API_KEY, from_email, to_emails)

    schedule.every(int(fetch)).hours.do(_fetch_tweet_job)
    schedule.every().day.at("01:00").do(_send_email)
    while True:
        schedule.run_pending()
        time.sleep(1)
