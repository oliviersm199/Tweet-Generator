# -*- coding: utf-8 -*-
'''
Upon initializing object, a JSON formatted document is created which is used
to generate a random walk. This will generate random text that occasionally
produces amusing sentences.
'''
import tweepy
import os
import sys
import json
import re
import random


class PersonTweeter:
    def __init__(self, twitter_id, tpck, tsck, tpak, tsak, load_tweets=True, proper_caps=True, remove_urls=True):
        '''
        Params:
            - twitter_id: TwitterID of User : Required
            - tpck: Public Consumer Key from Twitter API : Required
            - tsck: Secret Consumer Key from Twitter API : Required
            - tpak: Public Access Key from Twitter API : Required
            - tsak: Secret Access Key from Twitter API : Required
            - proper_caps: Set if the tweets should have capitalization corrected.
            - remove_urls: Set to True if you want urls removed from tweet.
        '''
        self.public_consumer_key = tpck
        self.secret_consumer_key = tsck
        self.public_access_key = tpak
        self.secret_access_key = tsak
        self.twitter_id = twitter_id
        self.tweets_loaded = load_tweets
        self.proper_caps = proper_caps
        self.remove_urls = remove_urls
        # Generating the json document
        if load_tweets:
            self._generate_json_doc()
            self._load_json_doc()

    def _load_json_doc(self, ):
        # Loading the json document into the object field.
        with open(self.twitter_id + ".json") as json_doc:
            self.json_tree = json.load(json_doc)

    def _check_url(self, w1, w2, w3):
        '''
        Method to check if a 3 tuple set contains a url.
        '''
        return not (re.match("http.*", w1) or re.match("http.*", w2) or re.match("http.*", w3))

    def _generate_json_doc(self, ):
        '''
        Goes through all quotes and generates a JSON Document with the following pattern:

        # "a b c a b k"
        # {'a b': ['c','k'], 'b c': ['a'], 'c a': ['b']}
        # Algorithm Inspired From:
        # http://stackoverflow.com/questions/5306729/how-do-markov-chain-chatbots-work/5307230#5307230
        '''
        # Get all the quotes
        quotes = [quote.text for quote in self.load_tweets()]

        # Set up a dictionary to store the quotes in a tree like structure
        markov_dict = {}

        # for each quote, set up all possible combinations
        for quote in quotes:
            for w1, w2, w3 in self._triple_sets(quote):
                # Do not allow the words to contain  "\"" and do not copy expressions that are urls.
                if self.remove_urls and self._check_url(w1, w2, w3):
                    markov_dict.setdefault(' '.join((w1, w2)), []).append(w3)

        # Prettyprint a sorted list of the markov dict into a text file
        json_text = json.dumps(markov_dict, indent=4, sort_keys=True)
        with open(self.twitter_id + ".json", "w") as f:
            f.write(json_text)

    def load_tweets(self, ):
        # using the tweepy library to retrieve user queries
        auth = tweepy.OAuthHandler(self.public_consumer_key, self.secret_consumer_key)
        auth.set_access_token(self.public_access_key, self.secret_access_key)
        api = tweepy.API(auth)
        return api.user_timeline(id=self.twitter_id, count=200)

    def _triple_sets(self, sentence):
        '''
        Helper method which will generate all possible combinations of (w1,w2,w3)
        in a single string.
        '''
        sentence_list = sentence.split()
        for i in range(len(sentence_list) - 2):
            yield (sentence_list[i], sentence_list[i + 1], sentence_list[i + 2])

    def _proper_capitalization(self, sentence):
        '''

        Ensure that the generated tweet has proper capitalization.

        '''
        sentence_list = sentence.split()

        # always capitalize the first letter
        for i, c in enumerate(sentence_list[0]):
            if c.isalpha():
                sentence_list[0] = sentence_list[0][:i] + sentence_list[0][i].upper() + sentence_list[0][i + 1:]

        # this regular expression checks to see if the word ends with a period, ex
        # clamation mark or
        for i in range(len(sentence_list) - 1):
            if re.match('\w+[.!?]$', sentence_list[i]):
                # check if it is a url
                if not re.match('\Ahttps\w+$', sentence_list[i + 1]):
                    sentence_list[i + 1] = sentence_list[i + 1].capitalize()

        return ' '.join(sentence_list)

    def generate_random_tweet(self, length=140):
        '''
        Using the document generated in the intialization step, generate a tweet
        by executing a random walk on the markov chain.
        '''
        if not self.tweets_loaded:
            _generate_json_doc(self, )
            _load_json_doc(self, )

        # Start with Empty String
        tweet = ""
        key = random.choice(list(self.json_tree.keys()))
        tweet += key.split(' ')[0] + ' '

        while len(tweet) < length:
            tweet += key.split(' ')[1] + ' '
            try:
                value = random.choice(self.json_tree[key])
            except KeyError as e:
                key = random.choice(list(self.json_tree.keys()))
            else:
                word1, word2 = key.split(" ")
                key = ' '.join([word2, value])
        if self.proper_caps:
            return self._proper_capitalization(tweet)
        else:
            return tweet
