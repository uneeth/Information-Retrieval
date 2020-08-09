import tweepy
from tweepy import OAuthHandler
import pprint
import json
import emoji

import re
import unidecode


def extract_emojis(str):
    return ','.join(c for c in str if c in emoji.UNICODE_EMOJI)


ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)  # ,parser=tweepy.parsers.JSONParser())

query = 'narendra modi'
new_tweets = api.search(q=query, count=100,
                        tweet_mode='extended')

c = 0
with open('C:\\Users\\akula\\Documents\\IR\\temp.json', 'w') as f:  # ,encoding='utf16') as f:
    f.write('[')
    for tweet in new_tweets:
        tweet_clean = re.sub(r"http\S+", '', str(tweet.full_text))  # to remove URLs
        tweet_clean = re.sub(r"#(\w+)", '', tweet_clean)  # to remove hashtags
        tweet_clean = re.sub(r"@(\w+)", '', tweet_clean)  # to remove mentions
        tweet_clean = ''.join('' if c in emoji.UNICODE_EMOJI else c for c in tweet_clean)  # to remove emoticons
        # tweet_clean = unidecode.unidecode(tweet_clean)
        tweet_f = {
            'topic': 'Topic',
            'country': 'Country',
            'tweet_text': tweet.full_text,  # unidecode.unidecode(tweet.full_text),
            'tweet_lang': tweet.lang,
            'text_' + tweet.lang: tweet_clean,
            'id': tweet.id,
            'hashtags': [i['text'] for i in tweet.entities['hashtags']],
            'mentions': [i['screen_name'] for i in tweet.entities['user_mentions']],
            'tweet_urls': [url['display_url'] for url in tweet.entities['urls']],
            'tweet_emoticons': extract_emojis(tweet.full_text),
            'tweet_date': str(tweet.created_at),
            'tweet_loc': tweet.coordinates["coordinates"] if tweet.coordinates != None else None
            # tweet.get('user', {}).get('location', {})
        }
        json.dump(tweet_f, f)
        if (tweet != new_tweets[-1]):
            f.write(',')
    f.write(']')
f.close()
