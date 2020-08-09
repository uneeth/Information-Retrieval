import json
import tweepy
from tweepy import OAuthHandler
import datetime as dt
import time
import os
import sys
import pprint
import re
import unidecode
import emoji


def extract_emojis(str):
    return ','.join(c for c in str if c in emoji.UNICODE_EMOJI)


# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = ''
ACCESS_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

country_count = {'usa': 0, 'india': 0, 'brazil': 0}  # 10,000 per category
lang_count = {'en': 0, 'es': 0, 'hi': 0}
topic_count = {
    'environment': 0,
    'crime': 0,
    'politics': 0,
    'social unrest': 0,
    'infra': 0
}
country_count_geo = {'usa': 0, 'india': 0, 'brazil': 0}  # 10,000 per category
date_count = {}
total = 0

# Load twitter API
# https://stackoverflow.com/questions/24002536/get-tweepy-search-results-as-json -- json parser
api = tweepy.API(auth)
print('Twitter API Loaded', '\n')

tweet_lookup = []


def get_tweet_id(api, date='', days_ago=9, query='a'):
    ''' Function that gets the ID of a tweet. This ID can then be
        used as a 'starting point' from which to search. The query is
        required and has been set to a commonly used word by default.
        The variable 'days_ago' has been initialized to the maximum
        amount we are able to search back in time (9).'''

    if date:
        # return an ID from the start of the given day
        td = date + dt.timedelta(days=1)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        try:
            tweet = api.search(q=query, count=1, until=tweet_date)
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            time.sleep(15 * 60)

            tweet = api.search(q=query, count=1, until=tweet_date)

    else:
        # return an ID from __ days ago
        td = dt.datetime.now() - dt.timedelta(days=days_ago)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        # get list of up to 10 tweets
        try:
            tweet = api.search(q=query, count=10, until=tweet_date)
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            time.sleep(15 * 60)

            tweet = api.search(q=query, count=10, until=tweet_date)

    print('search limit (start/stop):', tweet[0].created_at)

    # return the id of the first tweet in the list
    return tweet[0].id


# Writing as json file
def write_tweets(tweets, filename, topic, country):
    ''' Function that appends tweets to a file. '''
    with open(filename, 'a') as f:  # ,encoding='utf16') as f:
        f.write('[')
        for tweet in tweets:
            tweet_clean = re.sub(r"http\S+", '', str(tweet.full_text))  # to remove URLs
            tweet_clean = re.sub(r"#(\w+)", '', tweet_clean)  # to remove hashtags
            tweet_clean = re.sub(r"@(\w+)", '', tweet_clean)  # to remove mentions        
            tweet_clean = ''.join('' if c in emoji.UNICODE_EMOJI else c for c in tweet_clean)  # to remove emoticons
            # tweet_clean = unidecode.unidecode(tweet_clean)
            tweet_f = {
                'topic': topic,
                'country': country,
                'tweet_text': tweet.full_text,  # unidecode.unidecode(tweet.full_text),
                'tweet_lang': tweet.lang,
                'text_' + tweet.lang: tweet_clean,
                'id': tweet.id,
                'hashtags': [i['text'] for i in tweet.entities['hashtags']],
                'mentions': [i['screen_name'] for i in tweet.entities['user_mentions']],
                'tweet_urls': tweet.entities['urls'],
                'tweet_emoticons': extract_emojis(tweet.full_text),
                'tweet_date': str(tweet.created_at),
                'tweet_loc': tweet.coordinates["coordinates"] if tweet.coordinates != None else None
                # tweet.get('user', {}).get('location', {})
            }
            if (tweet.coordinates != None):
                country_count_geo[country] += 1
            json.dump(tweet_f, f)
            if (tweet != tweets[-1]):
                f.write(',')
            try:
                date_count[str(tweet.created_at).split(' ')[0]] += 1
            except:
                date_count[str(tweet.created_at).split(' ')[0]] = 1

        f.write(']')
        f.close()


# Searching

# It is possible that less than 'count' tweets can be returns. Hence, the loop is required

def tweet_search(api, query, max_tweets, max_id, since_id, geocode='NULL'):
    ''' Function that takes in a search string 'query', the maximum
        number of tweets 'max_tweets', and the minimum (i.e., starting)
        tweet id. It returns a list of tweepy.models.Status objects. '''
    searched_tweets = []
    while len(searched_tweets) < max_tweets:
        remaining_tweets = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=remaining_tweets,
                                    since_id=str(since_id),
                                    max_id=str(max_id - 1),
                                    tweet_mode='extended')  # extended mode won't work with RT #https://github.com/tweepy/tweepy/issues/974
            #                                   geocode=geocode)
            print('found', len(new_tweets), 'tweets')
            if not new_tweets:
                print('no tweets found')
                break
            # Duplicate tweet removal logic
            new_tweets_list = []
            for tweet in new_tweets:
                if tweet.full_text not in tweet_lookup:
                    new_tweets_list.append(tweet)
                    tweet_lookup.append(tweet.full_text)
            print('Added: ' + str(len(new_tweets_list)))
            if (len(new_tweets_list) > 0):
                searched_tweets.extend(new_tweets)
                max_id = new_tweets_list[-1].id

        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            count_list = [country_count, topic_count, lang_count, country_count_geo, date_count]

            # Storing stats in a seperate file
            F = open('C:\\Users\\akula\\Documents\\IR\\tweetCrawler\\' + 'stats.txt', 'w')

            for c in count_list:
                for i, j in c.items():
                    F.write(i + ' : ' + str(j) + '\n')
            F.write('Total : ' + str(total))
            F.close()

            for c in count_list:
                for i, j in c.items():
                    print(i + ':' + str(j) + '\n')
            print('Total : ' + str(total))

            print('(until:', dt.datetime.now() + dt.timedelta(minutes=15), ')')
            time.sleep(15 * 60)
            break  # stop the loop

    return searched_tweets, max_id


def search_list():
    country = [
        'usa',
        'india',  # ,
        'brazil'
    ]  # 10,000 per category
    lang_list = [
        'en',
        'hi',
        'es']
    topics = {
        'environment': ['amazon', 'amazon fire', 'forest', 'environmental', 'nature', 'farming', 'agriculture', 'extinct', 'weather', 'outbreak',
                        'contamination', 'pollution', 'wildlife-conservation', 'endangered-species', 'climate-change',
                        'global-warming', 'landslide', 'scarcountry', 'ocean-dump', 'oil-spill', 'GMO', 'deforestation',
                        'natural-disaster', 'overpopulation', 'soil-contamination', 'marine-life', 'calamity',
                        'drought', 'famine', 'flood', 'smog', 'acid-rain', 'storm'],
        'crime': ['suicide', 'rob', 'accuse', 'convict', 'money-laundering', 'trafficking', 'murder', 'suspect', 'cop',
                  'police', 'arrest', 'rape', 'sentenced', 'abduction', 'drug-abuse', 'fraud', 'violence', 'unlawful',
                  'homicide', 'genocide', 'theft', 'illegal', 'crime', 'detention', 'criminal', 'terrorism'],
        'politics': ['political', 'donald-trump', 'modi', 'bolsonaro', 'government', 'economy', 'assembly',
                     'senate', 'election', 'lok-sabha', 'rajya-sabha', 'PM', 'MP',
                     'parliament', 'minister', 'president', 'Congress', 'republican', 'democrat', 'BJP', 'white-house',
                     'UN', 'National-People’s-Congress', 'National-Assembly', 'REM-Republique-En-Marche', 'LR',
                     'Socialist-party', 'pheu-thai-party'],
        'social unrest': ['riot', 'social-unrest', 'anarchy', 'rebellion', 'controversy', 'protest', 'strike', 'bandh',
                          'agitation', 'up-roar', 'political-movement', 'social-revolution'],
        'infra': ['infrastructure', 'roadways', 'railways', 'waterlines', 'electical-grid', 'sanitation', 'gasline',
                  'bridge', 'tunnel', 'telecom', 'airport', 'transportation']
    }  # max 30 keywords OR seperated per search
    count = 0

    search_dict = {}

    for c in country:
        for topic, query in topics.items():
            for l in lang_list:
                Key = c + '_' + topic + '_' + l  # Key
                Value = ' OR '.join(query) + ' -RT ' + c + ' lang:' + l  # Value
                search_dict[Key] = Value
                count += 1

    # print(count)
    # print(list(search_dict.keys())[0])    
    # print(list(search_dict.values())[0])
    # print(list(search_dict.keys())[0].split(','))
    return search_dict


def main():
    global total
    ''' This is a script that continuously searches for tweets
        that were created over a given number of days. The search
        dates and search phrase can be changed below. '''

    # Search terms    

    ''' search variables: '''

    search_phrases = search_list()
    time_limit = 30  # runtime limit in hours
    max_tweets = 10000  # number of tweets per search (will be
    # iterated over) - maximum is 100
    min_days_old, max_days_old = 0, 1  # search limits 
    # gives current weekday from last week,
    # min_days_old=0 will search from right now    

    # loop over search items,
    # creating a new file for each
    for topic, query in search_phrases.items():

        # print(topic,':',query)

        ''' other variables '''
        json_file_root = 'C:\\Users\\akula\\Documents\\IR\\tweetCrawler\\'
        os.makedirs(os.path.dirname(json_file_root), exist_ok=True)
        read_IDs = False

        # open a file in which to store the tweets
        '''    
        if max_days_old - min_days_old == 1:
            d = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}'.format(d.year, d.month, d.day)
        else:

            d1 = dt.datetime.now() - dt.timedelta(days=max_days_old-1)
            d2 = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}_to_{3}-{4:0>2}-{5:0>2}'.format(
                  d1.year, d1.month, d1.day, d2.year, d2.month, d2.day)
        '''
        json_file = json_file_root + topic + '.json'
        if os.path.isfile(json_file):
            print('Appending tweets to file named: ', json_file)
            read_IDs = True

        # set the 'starting point' ID for tweet collection
        if read_IDs:
            # open the json file and get the latest tweet ID
            with open(json_file, 'r') as f:
                lines = f.readlines()
                max_id = json.loads(lines[-1])['id']
                print('Searching from the bottom ID in file')
        else:
            # get the ID of a tweet that is min_days_old
            if min_days_old == 0:
                max_id = -1
            else:
                max_id = get_tweet_id(api, days_ago=(min_days_old - 1))

        # set the smallest ID to search for
        since_id = get_tweet_id(api, days_ago=(max_days_old - 1))
        print('max id (starting point) =', max_id)
        print('since id (ending point) =', since_id)

        ''' tweet gathering loop  '''
        start = dt.datetime.now()
        end = start + dt.timedelta(hours=time_limit)
        count, exitcount = 0, 0
        while dt.datetime.now() < end:
            count += 1
            print('count =', count)
            # collect tweets and update max_id
            tweets, max_id = tweet_search(api, query, max_tweets,
                                          max_id=max_id, since_id=since_id)  # ,
            #                              geocode=[-99.1332, 19.4326,50])
            # write tweets to file in JSON format
            # print('Search complete')
            if tweets:
                tweet_count = len(tweets)
                c_t_l = topic.split('_')

                country_count[c_t_l[0]] += tweet_count
                lang_count[c_t_l[2]] += tweet_count
                topic_count[c_t_l[1]] += tweet_count
                total += tweet_count
                write_tweets(tweets, json_file, c_t_l[1], c_t_l[0])
                exitcount = 0

            else:
                exitcount += 1
                if exitcount == 3:
                    if topic == list(search_phrases.keys())[-1]:

                        f. = open(
                            'C:\\Users\\akula\\Documents\\IR\\tweetCrawler\\' + 'tweet_lookup.txt',
                            'w')
                        for tweet in tweet_lookup:
                            f.write(tweet)  # .encode('unicode-escape')
                        f.close()

                        F = open('C:\\Users\\akula\\Documents\\IR\\tweetCrawler\\' + 'stats.txt',
                                 'w')

                        for c in count_list:
                            for i, j in c.items():
                                F.write(i + ' : ' + str(j) + '\n')
                        F.write('Total : ' + str(total))
                        F.close()

                        for c in count_list:
                            for i, j in c.items():
                                print(i + ':' + str(j) + '\n')
                        print('Total : ' + str(total))

                        sys.exit('Maximum number of empty tweet strings reached - exiting')
                    else:
                        print('Maximum number of empty tweet strings reached - breaking')
                        break


if __name__ == "__main__":
    main()