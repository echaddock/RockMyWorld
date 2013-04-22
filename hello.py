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
FREEBASE_SEARCH_URL = "https://googleapis.com/freebase/v1/search?%s"

#Get freebase topic id
def get_topic_id(term):
	parser = OptionParser()
	parser.add_option("--query", dest="query", help="Freebase", default = "Google")
	parser.add_option("--max-results", dest="maxResults", help= "max youtube", default = 25)
	parser.add_option("--type", dest="type", help="youtube", default="channel")
	(options, args) = parser.parse_args()
	freebase_params = dict(query=options.query, key=DEVELOPER_KEY)
	freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
	freebase_response = json.loads(urllib.urlopen(freebase_url).read())
	#if len(freebase_response["result"]) == 0:
	#	exit("No matching terms were found in Freebase.")

	#mids = []
	#index = 1
	#print "The following topics were found:"
	#for result in freebase_response["result"]:
	#	return result.get("name", "Unknown")
    #print "  %2d. %s (%s)" % (index, result.get("name", "Unknown"),
      #result.get("notable", {}).get("name", "Unknown"))
    #index += 1

@app.route('/search/<search_term>')
def search_for_term(search_term):
	#Query database for search term, get tags. 
	parser = OptionParser()
	parser.add_option("--query", dest="query", help="Freebase search term", default="Google")
	(options, args) = parser.parse_args()
	freebase_params = dict(query=options.query, key=DEVELOPER_KEY)
	freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
	freebase_response = json.loads(urllib.urlopen(freebase_url).read())
	print freebase_response
	if len(freebase_response["result"]) == 0:
		exit("No matching terms were found in Freebase.")
# 	tag = query_for(free_base_term)

	#If not in database, call YouTube API with search term, get back ID 
#	if tag:
	#videoId = youtube_search(search_term)
	#tag artist with Emanuele's algorithms
	#tag = tag(videoId)

		#Add to database
	#add_to_db(songName, artistName, tag)

	#Query SeatGeek API, get back json list of local bands
	#For each band in result, get its tag
	#sort by tags
	#return this sorted object as json
	
	return 'Hello %s' % search_term

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
	c = conn.cursor()
	
	sql = 'select * from artists where name=term'
	

	conn.commit()
	conn.close()

def add_to_db(songName, artistName, tag):
	print 'addtodb'

if __name__ == '__main__':
	app.run()
