import re
import tweepy
from tweepy.api import API
from tweepy.auth import AuthHandler, OAuthHandler
from tweepy.cursor import Cursor
from tweepy import Stream
import ApiKey
import numpy as np
import pandas as pd
#questo file contiene una classe che ti permette di fare l outh a twitter developer
#scarica i 


class TwitterClient():
    #costruttore
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client=API(self.auth)
        self.twitter_user= twitter_user
    #metodo per estrarre i tweets piu recenti di un utente
    def get_user_timeline_tweets(self,num_tweets):
        tweets=[]
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_twitter_client_api(self):
        return self.twitter_client

class TwitterAuthenticator():
    #classe di autenticazione
    def authenticate_twitter_app(self):
        try:
            auth = OAuthHandler(ApiKey.consumer_key, ApiKey.consumer_secret)
            auth.set_access_token(ApiKey.access_token_key, ApiKey.access_token_secret)
        except: 
            print("Errore: Authenticazione Fallita") 
        return auth

       
class TwitterStreamer():
    # serve per creare uno Stream di Tweets in real time (usando le Twitter Streming API)
    def init(self):
        self.twitter_autenticator = TwitterAuthenticator()    

    def stream_tweets(self, hash_tag_list):
        listener = TwitterListener()
        auth = self.twitter_autenticator.authenticate_twitter_app() 
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


class TwitterListener(tweepy.StreamListener):

    def on_data(self, data):
        # metodo per ricevere i dati
        try:
            print(data)
            #qui devo passare i dati a kafaka?
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          
    # metodo per stampare lo stato di eventuali errori
    def on_error(self, status):
        if status == 420:
            return False
        print(status)
#metodo che ti serve per avere i dati del tweet sotto forma di data frame o anche grande tabella
def tweets_to_data_frame(tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['User'] = np.array([tweet.user.screen_name for tweet in tweets])
        df['position'] = np.array([tweet.user.location for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])   
        return df

