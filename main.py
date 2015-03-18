
__author__ = 'jml168@pitt.edu (J. Matthew Landis)'


import os
import logging
import pickle
import webapp2
import time
import httplib2
import json
import tweepy
import haigha
from haigha.connections.rabbit_connection import RabbitConnection
from apiclient import discovery
from oauth2client import appengine
from oauth2client import client
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
#######################################################################

PROJECTID = '934763316754'

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """""
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS

http = httplib2.Http(memcache)
service = discovery.build("plus", "v1", http=http)
bigquery_service = discovery.build("bigquery","v2", http=http)

consumer_key = "9xNrmD6hE0xnRSYdZt5t0XT0B"
consumer_secret = "kperqjklvPhBCVvHI96aZIfJu5w1DHI2BZoNMdBEvBPfmuZIYG"
access_token = "46501499-cijYvv9ixtQKHLSiLt9QaRtcmWeEKvvGZK5s6ukw7"
access_token_secret = "D127XCAN02BPb0ZtcreCG6dpBJyiiLCeD6ckS2MgdHqwG"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


decorator = appengine.oauth2decorator_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/plus.me',
    message=MISSING_CLIENT_SECRETS_MESSAGE)

bq_decorator = appengine.oauth2decorator_from_clientsecrets(
  CLIENT_SECRETS,
  scope='https://www.googleapis.com/auth/bigquery',
  message=MISSING_CLIENT_SECRETS_MESSAGE)

## Function to retrieve and render a template
def render_template(handler, templatename, templatevalues):
    path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
    html = template.render(path, templatevalues)
    handler.response.out.write(html)

#######################################################################
## Handles and loads index page
class MainPage(webapp2.RequestHandler):

    def get(self):
        nickname = "null"
        email = "null"
        user = users.get_current_user()
        login = users.create_login_url('/')
        logout = users.create_logout_url('/')
        os.system("python stream.py")
        if user != None:
            nickname = user.nickname()
            email = user.email()

        template_values = {
        'login': login,
        'logout': logout,
        'user': user,
        'nickname': nickname,
        'email': email
        }
        render_template(self, 'index.html', template_values)

#######################################################################
## Handle user info and profile
class CreateProfile(webapp2.RequestHandler):
    def get(self):
        template_data = {}
        template_path = 'templates/createProfile.html'
        self.response.out.write(template.render(template_path,template_data))


#######################################################################
## process user profile
## check for user signed in, if so, save the entered information, otherwise, redirect them to the login page
class ProcessUser(webapp2.RequestHandler) :

    def post(self) :
		user = users.get_current_user()
		if user:
			NewUser = UserModel()
			NewUser.uid = user.user_id()
			NewUser.fname = self.request.get('fname')
			NewUser.lname = self.request.get('lname')
			NewUser.location = self.request.get('location')
			NewUser.additional = self.request.get('additional')
			NewUser.words = []
			for word in words:
				NewUser.word+=[word]
			NewUser.put()
			self.redirect('/')
		else
			self.redirect(users.create_login_url('/'))

#######################################################################
## Model Data
class DataHandler(webapp2.RequestHandler) :

    @bq_decorator.oauth_aware
    def get(self) :
        if bq_decorator.has_credentials():
            http = bq_decorator.http()
            inputData = self.request.get("inputData")
            queryData = {'query':'SELECT SUM(word_count) as WCount,corpus_date,group_concat(corpus) as Work FROM '
'[publicdata:samples.shakespeare] WHERE word="'+inputData+'" and corpus_date>0 GROUP BY corpus_date ORDER BY WCount'}
            tableData = bigquery_service.jobs()
            dataList = tableData.query(projectId=PROJECTID,body=queryData).execute(http)

            resp = []
            if 'rows' in dataList:
                #parse dataList
                for row in dataList['rows']:
                    for key,dict_list in row.iteritems():
                        count = dict_list[0]
                        year = dict_list[1]
                        corpus = dict_list[2]
                        resp.append({'count': count['v'],'year':year['v'],'corpus':corpus['v']})
            else:
                resp.append({'count':'0','year':'0','corpus':'0'})
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))
        else:
            self.response.write(json.dumps({'error':'No credentials'}))


#######################################################################
## Model Words
class WordsHandler(webapp2.RequestHandler) :

    @bq_decorator.oauth_aware
    def get(self) :
        if bq_decorator.has_credentials():
            http = bq_decorator.http()
            inputData = self.request.get("inputData")
            queryData = {'query':'SELECT text FROM '
'[doctor-know:rtda.tweets] WHERE Words CONTAINS "'+inputData+'"GROUP BY text ORDER BY text LIMIT 150'}
            tableData = bigquery_service.jobs()
            dataList = tableData.query(projectId=PROJECTID,body=queryData).execute(http)

            resp = {}
            resp['text'] = status.text
            resp['created_at'] = time.mktime(status.created_at.timetuple())
            resp['geo'] = status.geo
            resp['source'] = status.source
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(resp))
        else:
            self.response.write(json.dumps({'error':'No credentials'}))


#######################################################################
## Profile Page
class ProfilePage(webapp2.RequestHandler) :

    def get(self):
        template_data = {}
        template_path = 'templates/profile.html'
        self.response.out.write(template.render(template_path,template_data))



#######################################################################
## Artificial Creativity Engine
class DisplayEngine(webapp2.RequestHandler) :

    def get(self):
        template_data = {}
        template_path = 'templates/engine.html'
        self.response.out.write(template.render(template_path,template_data))


#######################################################################
## Data Analysis
class DisplayData(webapp2.RequestHandler) :

    def get(self):
        template_data = {}
        template_path = 'templates/data.html'
        self.response.out.write(template.render(template_path,template_data))


#######################################################################
## Establish/Update User Profile
class UserModel(ndb.Model) :
	uid = ndb.StringProperty(indexed=True)
    fname = ndb.StringProperty(indexed = false)
    lname = ndb.StringProperty(indexed = false)
	location = ndb.StringProperty(indexed = false)
	additional = ndb.StringProperty(indexed = false)
	words = ndb.StringProperty(indexed=False,repeated=True)


#######################################################################
## Establish/Update User Profile
# class CustomStreamListener(tweepy.StreamListener):
#     def __init__(self, api):
#         self.api = api
#         super(tweepy.StreamListener, self).__init__()

#         #setup rabbitMQ Connection
#         self.connection = RabbitConnection(host='130.211.189.207', heartbeat=None, debug=True)

#         self.channel = self.connection.channel()

#         #set max queue size
#         args = {"x-max-length": 2000}

#         self.channel.queue.declare(queue='twitter_topic_feed', arguments=args)

#     def on_status(self, status):
#         print status.text, "\n"

#         data = {}
#         data['text'] = status.text
#         data['created_at'] = time.mktime(status.created_at.timetuple())
#         data['geo'] = status.geo
#         data['source'] = status.source

#         #queue the tweet
#         self.channel.basic.publish(exchange='',
#                                     routing_key='twitter_topic_feed',
#                                     body=json.dumps(data))

#     def on_error(self, status_code):
#         print >> sys.stderr, 'Encountered error with status code:', status_code
#         return True  # Don't kill the stream

#     def on_timeout(self):
#         print >> sys.stderr, 'Timeout...'
#         return True  # Don't kill the stream

# sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
# # my keyword today is chelsea as the team just had a big win
# sapi.filter(track=[self.request.get("inputData")])

app = webapp2.WSGIApplication( [
    ('/', MainPage),
    ('/profile', ProfilePage),
    ('/createProfile', CreateProfile),
    ('/userRegister', ProcessUser),
    ('/getData', DataHandler),
    ('/getWords', WordsHandler),
    ('/data', DisplayData),
    ('/engine', DisplayEngine),
    (decorator.callback_path, decorator.callback_handler()),
    (bq_decorator.callback_path, bq_decorator.callback_handler())
], debug=True)
