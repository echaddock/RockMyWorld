#!/usr/bin/python

from flask import Flask
from apiclient.discovery import build
from optparse import OptionParser

import json
import urllib
import sqlite3

app = (Flask)(__name__)
DEVELOPER_KEY = "AIzaSyD5c2xZv_wEoIzsQuEFFUFJyGj1hqHv_pg"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
FREEBASE_SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s"

@app.route('/search/<search_term>')
def search_for_term(search_term):
	topicName = get_topic_id(search_term) 

    #if this artist name is in the database, get its tag
	t = query_for(topicName)
	if(t):
		thistag = t

	#If not in database, tag it

	#Query SeatGeek for local events
	#Get tag of each artists/tag it if not tagged already
	#Find similarity between each artist and this artist
	#Sort accordingly
	#Return to the iOS app

	return youtube_search(topicName)


def get_topic_id(term):
	parser = OptionParser()
	parser.add_option("--query", dest="query", help="Freebase search term", default=term)
	(options, args) = parser.parse_args()
	freebase_params = dict(query=options.query, key=DEVELOPER_KEY)
	freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
	freebase_response = json.loads(urllib.urlopen(freebase_url).read())
	if len(freebase_response["result"]) == 0:
		exit("No matching terms were found in Freebase.")

 	return freebase_response["result"][0]["name"]

#Search the YouTube API for a video relating to a keyword

def youtube_search(term):
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
			developerKey=DEVELOPER_KEY)
	parser = OptionParser()
	parser.add_option("--query", dest="query", default=term)
	(options, args) = parser.parse_args()

	search_response = youtube.search().list(
			q=options.query,
			type = "video",
			part = "id",
			maxResults = 1
			).execute()


	return (search_response.get("items", [])[0]["id"]["videoId"])

def query_for(term):
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM artists WHERE name=:t", {"t": term})
	conn.commit()
	data = cur.fetchone()
	cur.close()
	return data	

if __name__ == "__main__":
	app.run()
