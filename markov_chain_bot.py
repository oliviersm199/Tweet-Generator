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
	def __init__(self,twitter_id,public_consumer_key, secret_consumer_key, public_access_key, secret_access_key,load_tweets=True):
		'''
		The object on construction takes the following parameters:
		    - twitter_id: The twitterID of the individual's tweets that you want to scrape
		    - public_consumer_key: Public Consumer Key from Twitter API
		    - secret_consumer_key: Secret Consumer Key from Twitter API
		    - public_access_key: Public Access Key from Twitter API
		    - secret_access_key: Secret Access Key from Twitter API
		'''
		self.public_consumer_key = public_consumer_key
		self.secret_consumer_key = secret_consumer_key
		self.public_access_key = public_access_key
		self.secret_access_key = secret_access_key
		self.twitter_id = twitter_id
		# Generating the json document
		if load_tweets:
			self._generate_json_doc()

		# Loading the json document into the object field.
		with open("tweets.json") as json_doc:
			self.json_tree = json.load(json_doc)

	def _get_tweets(self,):
		# using the tweepy library to retrieve user queries
		auth = tweepy.OAuthHandler(self.public_consumer_key,self.secret_consumer_key)
		auth.set_access_token(self.public_access_key,self.secret_access_key)
		api = tweepy.API(auth)
		return api.user_timeline(id=self.twitter_id,count=200)

	def _triple_sets(self,sentence):
		'''
		Helper method which will generate all possible combinations of (w1,w2,w3)
		in a single string.
		'''
		sentence_list = sentence.split()
		for i in range(len(sentence_list) - 2):
			yield (sentence_list[i], sentence_list[i+1],sentence_list[i+2])

	def _generate_json_doc(self,):
		'''

		Goes through all quotes and generates a JSON Document with the following pattern:

		# "a b c a b k"
		# {'a b': ['c','k'], 'b c': ['a'], 'c a': ['b']}
		# Algorithm Inspired From:
		# http://stackoverflow.com/questions/5306729/how-do-markov-chain-chatbots-work/5307230#5307230

		'''
		# Get all the quotes
		quotes = [quote.text for quote in self._get_tweets()]

		# Set up a dictionary to store the quotes in a tree like structure
		markov_dict = {}

		# for each quote, set up all possible combinations
		for quote in quotes:
			for w1,w2,w3 in self._triple_sets(quote):
				# Do not allow the words to contain  "\"" and do not copy expressions that are urls.
				if not re.match("http.*",w1) and not re.match("http.*",w2) and not re.match("http.*",w3):
					w1 = w1.replace("\"","")
					w2 = w2.replace("\"","")
					w3 = w3.replace("\"","")
					markov_dict.setdefault(unicode(' '.join((w1,w2))),[]).append(unicode(w3))

		# Prettyprint a sorted list of the markov dict into a the trump.json doc
		json_text = json.dumps(markov_dict,indent=4,sort_keys=True)
		with open("tweets.json","w") as f:
			f.write(json_text)

	def _proper_capitalization(self,sentence):
		'''

		Ensure that the generated tweet has proper capitalization.

		'''
		sentence_list = sentence.split()

		# always capitalize the first letter
		for i, c in enumerate(sentence_list[0]):
			if c.isalpha():
				sentence_list[0] = sentence_list[0][:i] + sentence_list[0][i].upper() + sentence_list[0][i+1:]

		# this regular expression checks to see if the word ends with a period, ex
		# clamation mark or
		for i in range(len(sentence_list)-1):
			if re.match('\w+[.!?]$',sentence_list[i]):
				#check if it is a url
				if not re.match('\Ahttps\w+$',sentence_list[i+1]):
					sentence_list[i+1] = sentence_list[i+1].capitalize()

		return ' '.join(sentence_list)

	def generate_random_tweet(self, length=140):
		'''
		Using the document generated in the intialization step, generate a tweet
		by executing a random walk on the markov chain.
		'''

		# Start with Empty String
		tweet = ""

		#Initial Starting Key
		key = random.choice(self.tweet_json.keys())

		while len(tweet) < length:
			try:
				value = random.choice(self.trump_json[trump_key])
			except KeyError as e:
				trump_tweet += '. '
				trump_value = random.choice(self.trump_json.keys())

			trump_tweet += ' '.join([trump_key,trump_value])

			# Getting second word in trump key to generate new key
			trump_second = trump_key.split(' ')[1]
			trump_key = ' '.join([trump_second,trump_value])

		return self._proper_capitalization(trump_tweet)
