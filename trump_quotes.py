# -*- coding: utf-8 -*-
'''

This module will retrieve the latest donald trump tweets and store in an sqlite database

'''
import tweepy
import os
from app import db, Quote
from sqlalchemy.sql.expression import func



class TrumpTweetRetriever:

	def __init__(self,consumer_key=         os.environ['TWITTER_PUBLIC_CONSUMER_KEY'],
					  consumer_secret=      os.environ['TWITTER_SECRET_CONSUMER_KEY'],
					  access_token =        os.environ['TWITTER_PUBLIC_ACCESS_KEY'],
					  access_token_secret = os.environ['TWITTER_SECRET_ACCESS_KEY']):

		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token = access_token
		self.access_token_secret= access_token_secret

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)

		self.TWITTER_ID = "25073877"

	def get_trump_tweets():
		'''
		Will add trump tweets based on the last trump tweet stored in the database.
		Initially the maximum # of tweets is 200. This would ideally be run as a cron job.
		'''
		try:
			max_id = db.session.query(func.max(Quote.twitter_id)).all()[0][0]
			result = api.user_timeline(id=TWITTER_ID,count=200,since_id=str(max_id))
		except IndexError:
			result = api.user_timeline(id=TWITTER_ID,count=200)

		for item in result:
			quote = Quote(trumpy=True,quote_text=item.text, twitter_id = item.id, twitter_account="realDonaldTrump")
			db.session.add(quote)

		db.session.commit()
