# -*- coding: utf-8 -*-
'''
Using Stored Trump Tweets, a chatbot will generate a JSON formatted document that I can then use to generate random tweets
of variable length.

'''
import json
import re
import random

class TrumpTweeter:
	def __init__(self,db,Quote):
		'''

		Initialize giving a SQLAlchemy Object Quote which contains the quotes
		from twitter. A JSON document will be generated in the current working
		directory which will be used in subsequent methods to generate Trump
		Tweets.

		'''
		# intiailizing the json doc to use as markov chain
		self.Quote = Quote
		self.db = db
		# Generating the json document
		self._generate_json_doc()

		# Loading the json document into the object field.
		with open("trump.json") as trump_json:
			self.trump_json = json.load(trump_json)

	def _triple_sets(self,sentence):
		'''
		Helper method which will generate all possible combinations of (w1,w2,w3)
		in a single string.
		'''
		sentence_list = sentence.split()
		for i in range(len(sentence_list) - 2):
			yield (sentence_list[i], sentence_list[i+1], sentence_list[i+2])

	def _generate_json_doc(self,):
		'''

		Goes through all quotes and generates a JSON Document with the following pattern:

		# "a b c a b k"
		# {'a b': ['c','k'], 'b c': ['a'], 'c a': ['b']}
		# Algorithm Inspired From:
		# http://stackoverflow.com/questions/5306729/how-do-markov-chain-chatbots-work/5307230#5307230

		'''
		# Get all the quotes
		quotes = self.Quote.query.all()

		# Set up a dictionary to store the quotes in a tree like structure
		markov_dict = {}

		# for each quote, set up all possible combinations
		for quote in quotes:
			for w1,w2,w3 in self._triple_sets(quote.quote_text):
				# Do not allow the words to contain  "\"" and do not copy expressions that are urls.
				if not re.match("http.*",w1) and not re.match("http.*",w2) and not re.match("http.*",w3):
					w1 = w1.replace("\"","")
					w2 = w2.replace("\"","")
					w3 = w3.replace("\"","")
					markov_dict.setdefault(unicode(' '.join((w1,w2))),[]).append(unicode(w3))

		# Prettyprint a sorted list of the markov dict into a the trump.json doc
		json_text = json.dumps(markov_dict,indent=4,sort_keys=True)
		with open("trump.json","w") as f:
			f.write(json_text)

	def generate_random_tweet(self,length=140):
		'''

		Using the document generated in the intialization step, generate a tweet
		by executing a random walk on the markov chain.

		'''
		trump_tweet = ""
		trump_key = random.choice(self.trump_json.keys())
		trump_tweet += trump_key.split(' ')[0] + ' '

		while len(trump_tweet) < length:
			trump_tweet += trump_key.split(' ')[1] + ' '
			try:
				trump_value = random.choice(self.trump_json[trump_key])
			except KeyError as e:
				trump_key = random.choice(self.trump_json.keys())

			else:
				word1, word2 = trump_key.split(" ")
				trump_key = ' '.join([word2,trump_value])

		return self._proper_capitalization(trump_tweet)


	def generate_fake_real_tweet(self,):
		'''
		Will generate a fake or random tweet with 50% probability
		'''
		# flipping a coin
		choice = random.randint(0,1)

		# This is the real option
		if choice==0:
			quote_number = random.randrange(0, self.db.session.query(self.Quote).count())
			quote_object = self.Quote.query.all()[quote_number]
			quote = {}
			quote['quote_text'] = quote_object.quote_text
			quote['id'] = quote_object.id

		else:
			quote = {}
			quote['quote_text'] = self.generate_random_tweet()
			quote['id'] = -1

		return quote

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
