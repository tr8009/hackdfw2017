from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify, Response

from test import *
import json

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('base.html') 
    #return render_template('bird/webgl_gpgpu_birds.html') 


@app.route("/hashtag", methods=['POST'])
def hashtag():
    hashtag_text = request.form.get('hashtag', None)
    api = TwitterClient()
    tweets_dict = api.get_tweets(query = hashtag_text)
    #print(tweets_dict)
    #tweets = [json.dumps(tweet) for tweet in tweets_dict]
    #print json.dumps(tweets_dict)
    return jsonify(tweets=tweets_dict)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
