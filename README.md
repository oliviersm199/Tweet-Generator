# Tweet Generator
The drump tweet generator uses a Markov chain finite state model to take a
particular user id from twitter and generate tweets based off of that person's
previous tweets. The tweets are stored in a JSON document which allows for random
walks of the tweets to occur.

## Goals:

- Simplify creating a basic Markov Chain Twitter Bot.
- Easy to read and provide an introduction to a simple way to create something intelligent!

## Some features include:

- Option to remove urls.
- Option for proper capitalization
- Output of the generated tree into a pretty JSON Format that you can review.
- Scraping of the Twitter API using the Tweepy Library



## Installation

git clone https://www.github.com/oliviersm199/Tweet-Generator
cd Tweet-Generator

TPCK,TSCK,TPAK,TSAK = '<public_consumer_key>','<secret_consumer_key>','<public_access_key>','<secret_access_key>'
import markov_chain_bot
twitter_bot = markov_chain_bot.PersonTweeter('25073877',TPCK,TSCK,TPAK,TSAK)
random_tweet = twitter_bot.generate_random_tweet()
print(random_tweet)
