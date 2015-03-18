import tweepy
import sys
import haigha
import json
import time

#get your own twitter credentials at dev.twitter.com
consumer_key = "9xNrmD6hE0xnRSYdZt5t0XT0B"
consumer_secret = "kperqjklvPhBCVvHI96aZIfJu5w1DHI2BZoNMdBEvBPfmuZIYG"
access_token = "46501499-cijYvv9ixtQKHLSiLt9QaRtcmWeEKvvGZK5s6ukw7"
access_token_secret = "D127XCAN02BPb0ZtcreCG6dpBJyiiLCeD6ckS2MgdHqwG"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        #setup rabbitMQ Connection
        self.connection = haigha.connections.RabbitConnection(host='130.211.189.207', heartbeat=None, debug=True)

        self.channel = self.connection.channel()

        #set max queue size
        args = {"x-max-length": 2000}

        self.channel.queue.declare(queue='twitter_topic_feed', arguments=args)

    def on_status(self, status):
        print status.text, "\n"

        data = {}
        data['text'] = status.text
        data['created_at'] = time.mktime(status.created_at.timetuple())
        data['geo'] = status.geo
        data['source'] = status.source

        #queue the tweet
        self.channel.basic.publish(exchange='',
                                    routing-key='twitter_topic_feed',
                                    body=json.dumps(data))

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True  # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True  # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
# my keyword today is chelsea as the team just had a big win
sapi.filter(track=[self.request.get("inputData")])