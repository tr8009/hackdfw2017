import re
import tweepy
import json
from secrets import *
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = TWITTER_CONSUMER_KEY
        consumer_secret = TWITTER_CONSUMER_SECRET 
        access_token = TWITTER_ACCESS_TOKEN
        access_token_secret = TWITTER_ACCESS_TOKEN_SECRET
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return analysis.sentiment.polarity
        elif analysis.sentiment.polarity == 0:
            return analysis.sentiment.polarity
        else:
            return analysis.sentiment.polarity

    def get_tweet_polarity(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        return analysis.sentiment.polarity

    def get_tweets(self, query, lang='en', count=100):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            #fetched_tweets = self.api.search(q = query)
            fetched_tweets = [tweet._json for tweet in tweepy.Cursor(self.api.search, q=query, count=count, lang=lang).items(count)]

            #print(count)
            print(len(fetched_tweets))

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                #parsed_tweet['text'] = tweet['text']
                # saving sentiment of tweet
                #parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet['text'])
                #saving polarity of tweet
                #parsed_tweet['polarity'] = self.get_tweet_polarity(tweet['text'])
                parsed_tweet['sentiment'], parsed_tweet['polarity'] = self.get_tweet_sentiment(tweet['text'])
                #saving favorites of tweet
                #parsed_tweet['favorites'] = tweet['favorite_count']
                #saving retweets of tweet
                #parsed_tweet['retweets'] = tweet['retweet_count']


                # appending parsed tweet to tweets list
                if tweet['retweet_count'] > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
def main(input, cnt):
    api = TwitterClient()

    #tweets = api.get_tweets(query = input, count = cnt)
    tweets = [tweet._json for tweet in tweepy.Cursor(api.api.search, q=input, count=200, lang='en').items(200)]
    print tweets[1]
    #print json.dumps(tweets[1]._json)
    print(tweets[0]['text'])
    print(len(tweets))

    #print("##########POSITIVE TWEETS##########")
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    #for tweet in range(0, len(ptweets)):
    #for tweet in ptweets[:10]:
        #print(tweet['text'])
        #print(tweet['sentiment'])
        #print(tweet['polarity'])

    #print("##########NEGATIVE TWEETS##########")
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    #for tweet in range(0, len(ntweets)):
    #for tweet in ntweets[:10]:
        #print(tweet['text'])
        #print(tweet['sentiment'])
        #print(tweet['polarity'])


if __name__ == "__main__":
    # calling main function
    main('Donald Trump', 100)
