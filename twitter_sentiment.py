import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
class TwitterClient(object):
    def __init__(self):
        consumer_key = 'qFr4nEXlDN6Hb7FrVfcwSBkrU'
        consumer_secret = 'Tdt8Uej3pgUTbwVS74KyzDz54uzwS3NiiH0qv3xcl2WBPnPO07'
        access_token = '1120505850466988032-aDgEl2bTl6DkEG1gMa8LaqbyHJnA0k'
        access_token_secret = 'mF9IeMrAQwL1vtnZOrgzbYpImfj8hn7P2Nv6PFISMoT9g'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        stop_words=set(stopwords.words('english'))
        a=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        a=a.split()
        a=[x for x in a if x not in stop_words]
        lemmatizer = WordNetLemmatizer()
        a=[lemmatizer.lemmatize(x) for x in a]
        a=' '.join(a)
        a=a.lower()
        return a



    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'pos'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'neg'

    def get_tweets(self, query, count =10):
        tweets = []
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.TweepError as e:
            print("Error : " + str(e))

def main():
    api = TwitterClient()
    # input for term to be searched and how many tweets to search
    q = raw_input("Enter the product name to be analysed: ")
    NoOfTerms = int(raw_input("Enter how many tweets to search: "))
    twt = api.get_tweets(query = q, count = NoOfTerms)
    ptweets = [tweet for tweet in twt if tweet['sentiment'] == 'pos']
    pp=100*len(ptweets)/len(twt)
    print(q+"'s positive reception score {} %"+ str(pp))
    ntweets = [tweet for tweet in twt if tweet['sentiment'] == 'neg']
    np=100*len(ntweets)/len(twt)
    print(q+"'s negative reception score {} %"+ str(np))
    
if __name__ == "__main__":
    # calling main function
    main()
