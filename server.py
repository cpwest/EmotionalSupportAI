

# Dependencies


import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1   import Features, EntitiesOptions, KeywordsOptions, EmotionOptions

import os
import csv
import time
import random
import requests as req
import datetime
import tweepy
import numpy as np
import pandas as pd

# Import API Keys
# from config import (consumer_key, consumer_secret, 
                    # access_token, access_token_secret)


is_prod = os.environ.get('IS_HEROKU', None)

consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_token_secret = os.environ['access_token_secret']



natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='f246d7f4-d9f0-4eaf-b832-b08f063b8d65',
  password='e5ZOMLB5730C',
  version='2018-03-16')




# Twitter Credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())




# Target Term

target_term = "#feelingsad"




# Define function
def EmotionAnalysis():
    
    # Search for all tweets
    public_tweets = api.search(target_term, count=10, result_type="recent", lang="en")
    
    analyzed_tweets = []
    
    # Loop through all tweets
    for tweet in public_tweets["statuses"]:
        
        # assign values to variables 
        tweet_text = tweet["text"]
        tweetId = tweet["id"]
        tweet_author = tweet["user"]["screen_name"]
        in_reply = tweet['in_reply_to_status_id_str']
        retweeted = tweet['retweeted']
        
        print(json.dumps(tweet, indent=2))
        
        print("in reply: " + str(in_reply))
        
        if tweetId not in analyzed_tweets:
            try:
                analyzed_tweets.append(tweetId)
                response = natural_language_understanding.analyze(
                    text= tweet_text,
                    features=Features(
                        emotion=EmotionOptions(
                        ))).get_result()
            
                jsonified_response = json.dumps(response, indent=2)
                sadness_level = json.loads(jsonified_response)["emotion"]["document"]["emotion"]["sadness"]
            
            except Exception:
                pass
            
            # create random integer
            randnum = random.randint(1, 8)

            if sadness_level > .80:
                try:
                     if in_reply is None:
                        if retweeted is False: 
                            # api.update_status("@"+ tweet_author + " Cheer Up! Try visiting our website, it might help! www.emotionalsupportai.org", in_reply_to_status_id = tweetId)
                            if randnum == 1:
                                api.update_status("@"+ tweet_author + " Cheer Up! Try visiting our website, it might help! www.emotionalsupportai.org. Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId)
                            elif randnum == 2:
                                api.update_status("@"+ tweet_author + " It's gonna be okay! Try visiting our website, it might help! www.emotionalsupportai.org. Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId)
                            elif randnum == 3:
                                api.update_status("@"+ tweet_author + " We're here for you! Try visiting our website, it might help! www.emotionalsupportai.org. Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId)
                            elif randnum == 4:
                                api.update_status("@"+ tweet_author + " Hang in there, it gets better! Try visiting our website, it might help! www.emotionalsupportai.org. Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId)
                            elif randnum == 5:
                                api.update_status("@"+ tweet_author + " Hey there! Seems like you might be having a rough time. Check out our website! www.emotionalsupportai.org. Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId)
                            elif randnum == 6:
                                api.update_status("@"+ tweet_author + " Bad days can be tough, go to www.emotionalsupportai.org for some tips to turn things around! Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId) 
                            elif randnum == 7:
                                api.update_status("@"+ tweet_author + " Remember you're not alone! Check out www.emotionalsupportai.org. Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId)
                            elif randnum == 8:
                                api.update_status("@"+ tweet_author + " Don't let the bad days get you down! Check out our website! www.emotionalsupportai.org. Don't want to hear from us? Just reply stop to this message", in_reply_to_status_id = tweetId)
                
                except Exception:
                    pass
                
            print("Tweet Author: " + tweet_author)
            print("Tweet ID: " + str(tweetId))
            print("Sadness Level: " + str(sadness_level))
            print("Tweet Text: " + tweet_text)
            print("Analyzed Tweets: " + str(analyzed_tweets))
            print(json.dumps(response, indent=2))
            

            
 
            

           
            
        if tweetId in analyzed_tweets:
            print("We already anayzed this tweet: " + str(tweetId))
        



# Run function at 3 hour intervals
while(True):
        EmotionAnalysis()
        time.sleep(10800)

