from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from api import api

import operator

app = Flask(__name__)
app.config['MONGO_USERNAME'] = 'oktaokat'
app.config['MONGO_PASSWORD'] = 'asdasdasd2017'

app.config['MONGO_HOST'] = 'ds056419.mlab.com'
app.config['MONGO_PORT'] = 56419
app.config['MONGO_DBNAME'] = 'okat'

mongo = PyMongo(app)


@app.route('/topwords', methods=['GET'])
def get_top_words():
	data = api()
	tweet = mongo.db.dataset.find()
	result = data.get_top_words(tweet)
	return jsonify(result)

	
@app.route('/popular/users', methods=['GET'])
def get_popular_users():
	data = api()
	tweet = mongo.db.dataset.find().distinct('fromuser')
	count_tweet = []
	for s in tweet:
			count_tweet.append({'fromuser': s ,'total_tweet': mongo.db.dataset.find({'fromuser':s}).count()})
	result = data.get_popular_users(count_tweet)
	return jsonify(result)

@app.route('/popular/mentions', methods=['GET'])
def get_popular_mentions():
	#initialize to db
	tweet = mongo.db.dataset.find({"mentions": { "$exists" : True}})
	data = api()
	result = data.get_popular_mentions(tweet)
	return jsonify(result)

@app.route('/hourly', methods=['GET'])
def get_hourly_tweet():
	data = api()
	tweet = mongo.db.dataset.find().sort("createdat",-1)
	result = data.get_hourly_tweet(tweet)
	return jsonify(result)
	



if __name__ == '__main__':
    app.run(debug=True)