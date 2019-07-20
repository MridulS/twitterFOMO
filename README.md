### twitterFOMO

Don't want to spend hours scrolling away on Twitter but also feel that your feed
is important to keep up with updates (fear of missing out).

Setup a cron job to send you daily updates of your Twitter feed in your inbox.


[Email at 00:01 server time, and fetch twitter updates at 01:00, 07:00, 13:00, 19:00. Make it hourly if you follow a LOT of people, as the API restricts to last 200 tweets on your homepage.
```
1 0 * * * Path_to/python3 Path_to/twitterFOMO/send_email.py >> Path_to/cron.log 2>&1
0 1,7,13,19 * * * Path_to/python3 Path_to/twitterFOMO/get_twitter_timeline.py >> Path_to/cron.log 2>&1
```

No more scrolling away!!

Currently it sends you tweets in the format
```
tweet text - user_name - link_to_tweet

tweet text - user_name - link_to_tweet

tweet text - user_name - link_to_tweet

```
