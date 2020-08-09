# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 23:16:11 2019

@author: akula
"""

from typing import List, Any, Union
from nltk.corpus import stopwords
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import re
import emoji
import unicodedata
import string
import time
from nltk.corpus import stopwords
import random
import re

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

try:

    tweetcount = 0
    # initialize a list to hold all the tweepy Tweets
    alltweets = []
    # file = open('HillaryClinton_Inda_tweets.json', 'w',encoding="utf-8")
    file = open("David_Replies.json", 'w', encoding='utf-8')  # change poi
    file_original = open("David_Replies_Original.json", 'w', encoding='utf-8')  # change poi

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.search(q='to:' + "davidmirandario", count=100, wait_on_rate_limit=True,
                            tweet_mode="extended")  ###change screen name

    # save most recent tweets
    alltweets.extend(new_tweets)

    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    # no emoji
    for tweet in new_tweets:
        if ("RT @" not in tweet.full_text):
            r1 = {}
            r2 = {}
            r3 = {}
            r4 = {}
            r5 = {}
            r6 = {}
            r7 = {}
            r8 = {}
            r9 = {}
            r10 = {}
            a = {}
            b = {}
            d = {}
            e = {}
            m = {}
            z = {}
            y = {}
            h = {}

            json_dump = json.dumps(tweet._json)

            tweetData = json.loads(json_dump)
            # print(tweetData)
            text_en1 = tweetData["full_text"]

            # Filtering out the retweets
            if not tweetData["retweeted"] and 'RT @' not in text_en1:
                r10 = {'verified': tweetData["user"]["verified"]}
                # Crawling the HashTags
                hash1 = re.findall(r"#(\w+)", text_en1)
                h = {'hashtags': ' '.join(map(str, hash1))}
                r1 = {'poi_name': "davidmirandario"}  ######changePOI
                r2 = {'poi_id': tweetData["in_reply_to_user_id_str"]}
                r3 = {"country": "Brazil"}  ######change country
                r4 = {"replied_to_user_id": tweetData["in_reply_to_user_id_str"]}
                r6 = {"tweet_lang": tweetData["lang"]}
                if tweetData["lang"] == 'ne':
                    r6 = {"tweet_lang": 'en'}
                links = re.findall(r"(\w+:\/\/\S+)", text_en1)
                r7 = {"tweet_urls": ' '.join(map(str, links))}
                # r8={"reply_text":None}
                r9 = {"replied_to_tweet_id": tweetData["in_reply_to_status_id_str"]}
                emojis_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
                r = re.compile('|'.join(re.escape(p) for p in emojis_list))
                aux = [' '.join(r.findall(s)) for s in text_en1]
                e = {'tweet_emoticons': ' '.join(map(str, list(set(aux))))}

                c = (time.strftime('%Y-%m-%dT%H:00:00Z', time.strptime(tweetData['created_at'],
                                                                       '%a %b %d %H:%M:%S +0000 %Y')))

                y = {"tweet_date": c}

                result = re.findall("@([a-zA-Z0-9]{1,15})", text_en1)

                m = {'mentions': ' '.join(map(str, result))}

                b = {'city': 'Brasilia'}  ##########change city

                # Tweet Location : NYC
                d = {'tweet_loc': '15.8267, 47.9218'}  ###########change location

                # Regex to crawl the emoticons from twitter
                text_enc = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(:D)|(\w+:\/\/\S+)", " ", text_en1).split())
                text_upper = emoji_pattern.sub(r'', text_enc)
                text = text_upper.lower()
                text1 = ' '.join([word for word in text.split() if word not in (stopwords.words('english'))])
                text3 = ' '.join(word.strip(string.punctuation) for word in text1.split())
                text4 = re.sub(r'[!|@|#|%|&|\(|\)|\[|\]|\{|\}|\;|\:|\,|\/|<|>|\?|\`|\~|\-|\=|\_|\'|\"]', r' ', text3)
                text5 = text4.replace('"', '')
                text6 = text5.replace("'", "")
                text7 = text6.replace("?", " ")
                text8 = text7.replace("`", "")
                text9 = text8.replace("(", "")
                text10 = text9.replace(")", "")
                text11 = re.sub(r'[[0-9]', r'', text10)
                text12 = text11.replace("|", " ")
                text13 = text12.replace("‘", "")
                text14 = text13.replace("“", "")
                text15 = text14.replace("”", "")
                text16 = text15.replace("।", " ")
                text2 = text16.replace("’", "")
                text_en2 = re.sub(r'[\n]', r' ', text_en1)
                r5 = {"tweet_text": text_en2}
                r8 = {"reply_text": text_en2}
                # Checking for tweets in various languages : English, Hindi, Spanish
                if tweetData['lang'] == 'en':
                    z = {'text_en': text2}
                elif tweetData['lang'] == 'hi':
                    z = {'text_hi': text2}
                elif tweetData['lang'] == 'pt':
                    z = {'text_pt': text2}
                elif tweetData['lang'] == 'ne':
                    z = {'text_hi': text2}
                else:
                    z = {'text_en': text2}
                if tweetData["lang"] == 'ne':
                    tweetData["lang"] = 'en'

                #             print("Writing to Json")

                #             tweetData.update(b)
                tweetData.update(y)
                tweetData.update(d)
                tweetData.update(m)
                tweetData.update(z)
                tweetData.update(h)
                tweetData.update(e)
                tweetData.update(r1)
                tweetData.update(r2)
                tweetData.update(r3)
                tweetData.update(r4)
                tweetData.update(r5)
                tweetData.update(r6)
                tweetData.update(r7)
                tweetData.update(r8)
                tweetData.update(r9)
                tweetData.update(r10)
                json.dump(tweetData, file, ensure_ascii=False)
                file.write("\n")
                json.dump(tweet._json, file_original, ensure_ascii=False)
                file_original.write("\n")
                tweetcount += 1
                print("Tweetcount", tweetcount, tweetData["created_at"])

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        print("getting tweets before", oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.search(q='to:' + "davidmirandario", count=100, max_id=oldest, wait_on_rate_limit=True,
                                tweet_mode="extended")  ###change screen name

        # save most recent tweets
        alltweets.extend(new_tweets)
        for tweet in new_tweets:
            if ("RT @" not in tweet.full_text):
                a = {}
                b = {}
                d = {}
                e = {}
                m = {}
                z = {}
                y = {}
                h = {}
                r1 = {}
                r2 = {}
                r3 = {}
                r4 = {}
                r5 = {}
                r6 = {}
                r7 = {}
                r8 = {}
                r9 = {}
                r10 = {}

                json_dump = json.dumps(tweet._json)

                tweetData = json.loads(json_dump)
                text_en1 = tweetData["full_text"]

                # Filtering out the retweets
                if not tweetData["retweeted"] and 'RT @' not in text_en1:
                    r10 = {'verified': tweetData["user"]["verified"]}
                    # Crawling the HashTags
                    hash1 = re.findall(r"#(\w+)", text_en1)
                    h = {'hashtags': ' '.join(map(str, hash1))}
                    r1 = {'poi_name': "davidmirandario"}  ####changePOI
                    r2 = {'poi_id': tweetData["in_reply_to_user_id_str"]}
                    r3 = {"country": "Brazil"}  #####change country
                    r4 = {"replied_to_user_id": tweetData["in_reply_to_user_id_str"]}
                    r6 = {"tweet_lang": tweetData["lang"]}
                    if tweetData["lang"] == 'ne':
                        r6 = {"tweet_lang": 'en'}
                    links = re.findall(r"(\w+:\/\/\S+)", text_en1)
                    r7 = {"tweet_urls": ' '.join(map(str, links))}

                    r9 = {"replied_to_tweet_id": tweetData["in_reply_to_status_id_str"]}
                    emojis_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
                    r = re.compile('|'.join(re.escape(p) for p in emojis_list))
                    aux = [' '.join(r.findall(s)) for s in text_en1]
                    e = {'tweet_emoticons': ' '.join(map(str, list(set(aux))))}

                    c = (time.strftime('%Y-%m-%dT%H:00:00Z', time.strptime(tweetData['created_at'],
                                                                           '%a %b %d %H:%M:%S +0000 %Y')))

                    y = {"tweet_date": c}

                    result = re.findall("@([a-zA-Z0-9]{1,15})", text_en1)

                    m = {'mentions': ' '.join(map(str, result))}

                    b = {'city': 'Brasilia'}  ###change city

                    # Tweet Location : NYC
                    d = {'tweet_loc': '15.8267, 47.9218'}  ####change location

                    # Regex to crawl the emoticons from twitter
                    text_enc = ' '.join(
                        re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(:D)|(\w+:\/\/\S+)", " ", text_en1).split())
                    text_upper = emoji_pattern.sub(r'', text_enc)
                    text = text_upper.lower()
                    text1 = ' '.join([word for word in text.split() if word not in (stopwords.words('english'))])
                    text3 = ' '.join(word.strip(string.punctuation) for word in text1.split())
                    text4 = re.sub(r'[!|@|#|%|&|\(|\)|\[|\]|\{|\}|\;|\:|\,|\/|<|>|\?|\`|\~|\-|\=|\_|\'|\"]', r' ',
                                   text3)
                    text5 = text4.replace('"', '')
                    text6 = text5.replace("'", "")
                    text7 = text6.replace("?", " ")
                    text8 = text7.replace("`", "")
                    text9 = text8.replace("(", "")
                    text10 = text9.replace(")", "")
                    text11 = re.sub(r'[[0-9]', r'', text10)
                    text12 = text11.replace("|", " ")
                    text13 = text12.replace("‘", "")
                    text14 = text13.replace("“", "")
                    text15 = text14.replace("”", "")
                    text16 = text15.replace("।", " ")
                    text2 = text16.replace("’", "")
                    text_en2 = re.sub(r'[\n]', r' ', text_en1)
                    r5 = {"tweet_text": text_en2}
                    r8 = {"reply_text": text_en2}

                    # Checking for tweets in various languages : English, Hindi, Spanish
                    if tweetData['lang'] == 'en':
                        z = {'text_en': text2}
                    elif tweetData['lang'] == 'hi':
                        z = {'text_hi': text2}
                    elif tweetData['lang'] == 'pt':
                        z = {'text_pt': text2}
                    elif tweetData['lang'] == 'ne':
                        z = {'text_hi': text2}
                    else:
                        z = {'text_en': text2}
                    if tweetData["lang"] == 'ne':
                        tweetData["lang"] = 'en'
                    #                 tweetData.update(b)
                    tweetData.update(y)
                    tweetData.update(d)
                    tweetData.update(m)
                    tweetData.update(z)
                    tweetData.update(h)
                    tweetData.update(e)
                    tweetData.update(r1)
                    tweetData.update(r2)
                    tweetData.update(r3)
                    tweetData.update(r4)
                    tweetData.update(r5)
                    tweetData.update(r6)
                    tweetData.update(r7)
                    tweetData.update(r8)
                    tweetData.update(r9)
                    tweetData.update(r10)
                    json.dump(tweetData, file, ensure_ascii=False)
                    file.write("\n")
                    json.dump(tweet._json, file_original, ensure_ascii=False)
                    file_original.write("\n")
                    tweetcount += 1
                    print("Tweetcount", tweetcount, tweetData["created_at"])

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("tweets downloaded so far", len(alltweets))

except BaseException as ee:
    print("Error on_data: %s" % str(ee))

    # print(c)
file.close()
file_original.close()
