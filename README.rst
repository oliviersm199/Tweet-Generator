===============
Tweet Generator
===============
The tweet generator uses a Markov chain finite state model to take a
particular user id from twitter and generate tweets based off of that person's
previous tweets. The tweets are stored in a JSON document which allows for random
walks of the tweets to occur.

=====
Goals
=====

- Simplify creating a basic Markov Chain Twitter Bot.
- Easy to read and provide an introduction to a simple way to create something intelligent!

=====================
Features
=====================

- Option to remove urls.
- Option for proper capitalization
- Output of the generated tree into a pretty JSON Format that you can review.
- Scraping of the Twitter API using the Tweepy Library

============
Installation
============

To install, use pip ::

    pip install tweet-generator

=======
Example
=======

See the following example::

    from tweet_generator import tweet_generator
    TPCK = '<public_consumer_key>'
    TSCK = '<secret_consumer_key>'
    TPAK = '<public_access_key>'
    TSAK = '<secret_access_key>'
    twitter_bot = tweet_generator.PersonTweeter('25073877',TPCK,TSCK,TPAK,TSAK)
    random_tweet = twitter_bot.generate_random_tweet()
    print(random_tweet)