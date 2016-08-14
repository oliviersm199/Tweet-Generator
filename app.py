# -*- coding: utf-8 -*-
'''
This is a simple web application built to get people to guess if a series of quotes were said or not said by Donald Trump.

The intent of this application is not to be political but act a source of entertainment.

'''
from flask import Flask, render_template, request
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy
from markov_chain_bot import TrumpTweeter
import random


# Flask Application Initialization
app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

# Database Setup
class Quote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	trumpy = db.Column(db.Boolean,nullable=False)
	quote_text = db.Column(db.Text,nullable=False)
	twitter_id = db.Column(db.Integer,nullable=False)
	twitter_account = db.Column(db.Text,nullable=False)
	attempts = db.Column(db.Integer,default=0)
	correct_attempts = db.Column(db.Integer,default=0)


@app.route('/')
def main_page():
	trump_tweeter = TrumpTweeter(db,Quote)
	quote = trump_tweeter.generate_fake_real_tweet()
	return render_template("index.html",quote=quote)



if __name__ == '__main__':
	app.run(host="127.0.0.1",port=5001,debug=True,threaded=True)
