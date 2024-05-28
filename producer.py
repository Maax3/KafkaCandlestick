import datetime
import json
import time
import tweepy

from kafka import KafkaProducer

# twitter setup
# configured at https://apps.twitter.com/
consumer_key = 'lctYH5OBmIOARa7D4SyNSXQPX'
consumer_secret = 'PpPKCSNFBAJbFRfGYe79pzEz3t1MTnUbvDO3CiSeT0zH73JOFP'
access_token = '732718446-yx9Skb1e1Er9ci8WOBA6PO9wBFt3jmoPKlkb8APV'
access_token_secret = 'udWTbfWkXtLdQanZ1HE6MwUDVd7yzl0r1uuYkchxQJCHD'

# create anthentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# set access tokens and secret
auth.set_access_token(access_token, access_token_secret)
# create API object
api = tweepy.API(auth)

# kafka broker
# configured locally with HDP 2.6 sandbox
# need to add an entry for the sandbox in /etc/hosts
# Note: using localhost or 127.0.0.1 for kafka broker setting here doesn't work
kafka_brokers = 'sandbox-hdp.hortonworks.com:6667'
topic_name = 'tweets'
important_fields = ['created_at', 'id', 'id_str', 'text', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'lang']

# kafka producer
producer = KafkaProducer(
    bootstrap_servers=kafka_brokers,
    api_version=(0, 10, 1)
)


def get_tweets():

    res = api.search('kafka')

    for r in res:

        tweet = {k: r._json[k] for k in important_fields}
        tweet['text'] = tweet['text'].replace("'", "").replace("\"", "").replace("\n", "")
        producer.send(topic_name, str.encode(json.dumps(tweet)))


def stream(interval):

    while True:

        get_tweets()
        print('Streaming Tweets at {}'.format(str(datetime.datetime.now())))
        time.sleep(interval)

if __name__ == "__main__":
    stream(10)
