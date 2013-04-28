#!/usr/bin/python

from flask import Flask
from apiclient.discovery import build
from optparse import OptionParser

import json
import urllib
import sqlite3
import collections

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
	else:
		thistag = getTag(youtube_search(topicName))
		add_to_db(topicName, thistag)

	#Query SeatGeek for local events
	json_data = urllib.urlopen('http://api.seatgeek.com/2/events?geoip=true&per_page=50').read()
	data = json.loads(json_data)["events"] 

	eventsList = [] 
	#print eventsJSON
	#for each event, see if it is a music event and if it is get its tag
	for event in data:
		performers = event["performers"]
		place = event["venue"]
		date = event["datetime_local"]
		url = event["url"]
		for performer in performers:
			if(performer["type"] == "band"):
				name = performer["name"]
				t = query_for(name)
				if(t):
					currtag = t
				else:
					currtag = getTag(youtube_search(name))
					add_to_db(name, currtag)
				thisscore = get_score(event)
				e = {'name': name, 'location': place, 'date': date, 'url': url}
				eventsList.append((e, thisscore))
	#Sort events
	sortedList = sorted(eventsList, key = lambda event: event[1], reverse=True)	
	events = [event for (event, score) in sortedList]	
	return json.dumps(events) 

def get_score(event):
	return event["score"] #TODO for now just using the seatgeek popularity score
	
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

def getTag(youtubeID):
	#TODO
	return "pop"

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
	cur.execute("SELECT tag FROM artists WHERE name=:t", {"t": term})
	conn.commit()
	data = cur.fetchone()
	cur.close()
	return data	

def add_to_db(name, tag):
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()
	cur.execute('insert into artists (tag, name) values (?, ?)', (tag, name))
	conn.commit()
	cur.close()

if __name__ == "__main__":
	app.run()
