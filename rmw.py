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

#Echo Nest Stuff
from pyechonest import config
config.ECHO_NEST_API_KEY = "Q1TFFOJJLUTWJ5OPH"
from pyechonest import artist

@app.route('/search/')
def noQueryTerm():
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
				thisscore = event["score"]
				e = {'name': name, 'location': place, 'date': date, 'url': url}
				eventsList.append((e, thisscore))
	#Sort events
	sortedList = sorted(eventsList, key = lambda event: event[1], reverse=True)	
	events = [event for (event, score) in sortedList]	
	return json.dumps(events) 

@app.route('/search/<search_term>')
def search_for_term(search_term):
	artistName = get_topic_id(search_term) 

	try:
		a = artist.Artist(artistName) #could optimize this using database
	except Exception as e:
		print e
		return noQueryTerm()

	terms = query_for(a, artistName) #artist name
	return search_with_terms(terms)

#Does all the work for both artist and term search
def search_with_terms(terms):
 	artistProfile = dict() 
	for genre in terms:
		artistProfile[genre['name']] = genre['weight']
	#elif t:
	#	thistag = t
	#else:
	#	videoId = youtube_search(artistName)
	#	if(videoId == None): #error catching, no query
	#		return noQueryTerm()

	#	thistag = getTag(videoId)
	#	add_to_db(artistName, thistag)

	#Query SeatGeek for local events

	json_data = urllib.urlopen('http://api.seatgeek.com/2/events?geoip=true&per_page=80').read()
	data = json.loads(json_data)["events"] 
	eventsList = [] 

	for event in data:
		performers = event["performers"]
		place = event["venue"]
		date = event["datetime_local"]
		url = event["url"]
		for performer in performers:
			if(performer["type"] == "band"):
				name = performer["name"]
				artistID = performer["id"]
				thisscore = get_score(artistID, artistProfile, name) 
				if(thisscore > 80):
				 	continue
				e = {'name': name, 'location': place, 'date': date, 'url': url}
				eventsList.append((e, thisscore))

	#Sort events
	sortedList = sorted(eventsList, key = lambda event: event[1])	
	events = [event for (event, score) in sortedList]
	return json.dumps(events) 

@app.route('/genre/<genre_list>')
def parse_terms(genre_list):
 	terms = list()
	for term in genre_list.split(","):
		subdict = dict()
		subdict['name'] = term 
		subdict['weight'] = 1 
		terms.append(subdict)
	return search_with_terms(terms)


#Calculate similarity score for this artist
def get_score(artistID, baseArtist, artistName):
 	print "get score"
 	try:
		a = artist.Artist('seatgeek:artist:%s' % artistID)
	except Exception as e:
	 	print e
	 	print 'Artist not found'
	 	return 1000 # bad entry

	score = 0

	try:
		terms = query_for(a, artistName) 
	except:
	 	print 'terms fail'
		return 1000 # bad 

	for genre in terms:
		if genre['name'] in baseArtist.keys():
			score += abs(genre['weight'] - baseArtist[genre['name']])
		else:
			score += genre['weight'] 
	
	#Look for genres in base artist that are not in this artist
	for genreName in baseArtist.keys():
		if(genreName not in terms):
	 		score += baseArtist[genreName]
	print "return"
	return score



def get_topic_id(term):
	parser = OptionParser()
	parser.add_option("--query", dest="query", help="Freebase search term", default=term)
	(options, args) = parser.parse_args()
	freebase_params = dict(query=options.query, key=DEVELOPER_KEY)
	freebase_url = FREEBASE_SEARCH_URL % urllib.urlencode(freebase_params)
	freebase_response = json.loads(urllib.urlopen(freebase_url).read())
	if len(freebase_response["result"]) == 0:
		return ""
 	return freebase_response["result"][0]["name"]


def getTag(youtubeID):
	#TODO Emanuele's code
	return ""


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
	if(len(search_response.get("items", [])) == 0):
		return None 

	return (search_response.get("items", [])[0]["id"]["videoId"])


#query database or EchoNest API for an artist's terms
def query_for(artistObject, artistName):

 	#connect to database
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()

	#find the artist in artist table
	cur.execute("SELECT artistID FROM artists WHERE name=:t", {"t": artistName})
	conn.commit()
	fetch = cur.fetchone()
	if(fetch):
		artistID = fetch[0]
	else:
	 	#Get terms from echonest if artist not in database
		termsAndWeights = artistObject.get_terms()
		add_to_db(artistName, termsAndWeights)
		return termsAndWeights 

	try:
		cur.execute("SELECT termName, weight FROM terms, link WHERE \n\
		  (link.termID = terms.termID AND link.artistID=:a)", {"a": artistID})
	except Exception as e:
	 	print e

	conn.commit()
	termsAndWeights = cur.fetchall()
	cur.close()

	#Query Echonest if not in DB
	try:
		if(termsAndWeights):
		 	#reformat output!!
			reformat = list()
			for entry in termsAndWeights:
			 	subdict = dict()
				subdict['name'] = entry[0]
				subdict['weight'] = entry[1]
				reformat.append(subdict)
			return reformat 
		else:
			termsAndWeights = artistObject.get_terms()
			add_to_db(artistName, termsAndWeights)
	except Exception as e:
	 	print e
		return null
	return termsAndWeights



#Helper func to get a list of all terms for insert statement
def term_gen(terms):
	for term in terms:
	 	yield (term['name'],)



#Add artist -> terms mappings to database
def add_to_db(name, terms):
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()

	#Add each artist to the artists table
	cur.execute('insert into artists (name) values (?)', (name,))
	artistID = cur.lastrowid;

	#Add each term's name to the terms table
	for term in terms:
		try:
			cur.execute("select termID from terms where termName \n\
			  =:n", {'n': term['name']})
			termID = cur.fetchone()
			if(not termID):
				cur.execute('insert into terms (termName) values (?)', (term['name'],))  
				termID = cur.lastrowid
		 	else:
		 		termID = termID[0]

			#Add link
			cur.execute("insert into link (termID, artistID, weight) \n\
			  values (?, ?, ?)", (termID, artistID, term['weight']))
		except Exception as e:
		 	print e

	conn.commit()
	cur.close()

if __name__ == "__main__":
	app.run()
