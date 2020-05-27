import os
import json
from tqdm import tqdm

from congresstweets.Parsing.TweetParser import TweetParser

BASEPATH = '/home/scott/Documents/git/congresstweets/data'


class CongressTweets:

    def __init__(self, base_path):
        self.base_path = base_path
        self.tweets = []
        self.distinct_names = None

    def load(self, filename, display_stats=False):
        file = os.path.join(self.base_path, filename)
        if display_stats:
            print(f'loading payload from {filename}')
        before_count = len(self.tweets)
        with open(file) as f:
            for line in f:
                tweets = json.loads(line)
                for tweet in tweets:
                    self.tweets.append(tweet)
        amt = len(self.tweets) - before_count
        if display_stats:
            print(f'Read {amt} tweets.')

    def load_all(self):
        from os import listdir
        from os.path import isfile, join
        only_files = [f for f in listdir(self.base_path) if isfile(join(self.base_path, f))]
        only_json_files = [f for f in only_files if f.endswith('.json')]
        for i in tqdm(range(len(only_json_files))):
            self.load(only_json_files[i])
        count = len(self.tweets)
        print(f'Found {count} total tweets')

    @staticmethod
    def validate_tweet(tweet):
        if 'screen_name' not in tweet:
            return False
        if tweet['text'].strip().startswith('RT'):
            return False
        return True

    def sanitize_data(self):
        print('Sanitizing data')
        self.tweets = [tweet for tweet in tqdm(iter(self.tweets)) if self.validate_tweet(tweet)]


    def get_stats(self):
        self.distinct_names = {t['screen_name'] for t in self.tweets}

    def get_distinct_names(self):
        return self.distinct_names

    def get_tweets(self):
        return self.tweets

    def group_tweets_by_screen_name(self):
        group = dict()
        print('Grouping tweets by screen name.')
        for i in tqdm(range(len(self.tweets))):
            tweet = self.tweets[i]
            screen_name = tweet['screen_name']
            if screen_name in group:
                old = group[screen_name]
                old.append(tweet)
                group[screen_name] = old
            else:
                group[screen_name] = list(tweet)
        return group

    def compute_hash_tag_frequencies(self):
        parser = TweetParser()
        hash_tag_dict = dict()
        for i in tqdm(range(len(self.tweets))):
            tweet = self.tweets[i]['text']
            hash_tags = parser.get_hash_tags(tweet)
            for hash_tag in hash_tags:
                old_count = 0
                if hash_tag in hash_tag_dict:
                    old_count = hash_tag_dict[hash_tag]
                hash_tag_dict[hash_tag] = old_count + 1
        hash_tag_freq = [{'word': key, 'count': value} for key, value in hash_tag_dict.items()]
        return hash_tag_freq



if __name__ == "__main__":
    src = CongressTweets(BASEPATH)
    src.load_all()
    #src.load('2020-05-20.json')

    print(f'Found {len(src.get_tweets())} raw tweets.')
    src.sanitize_data()
    print(f'Sanitized count is {len(src.get_tweets())} tweets.')
    src.get_stats()
    distinct = src.get_distinct_names()
    grouped = src.group_tweets_by_screen_name()
    print("Finding distinct hash-tags")
    hash_tag_frequencies  = src.compute_hash_tag_frequencies()
    print(f"Found {len(hash_tag_frequencies)} distinct hash-tags")

    hash_tag_frequencies.sort(key=lambda x: x['count'], reverse=True)

    pass