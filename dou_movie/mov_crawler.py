#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import time
import json
import requests
from bs4 import BeautifulSoup

DOU_MOVIE_URL_PREFIX = "https://movie.douban.com/people"
DOU_MOVIE_URL_MIDFIX = "collect?start="
DOU_MOVIE_URL_SUFFIX = "&sort=time&rating=all&filter=all&mode=grid"

class Movie(object):
	"""docstring for ClassName"""
	def __init__(self, name, intro):
		super(Movie, self).__init__()
		self.name = name
		self.intro = intro

def dou_movie_url_generator(people_name):
	START_POINT = 0
	STEP_NUM = 15
	while True:
		yield DOU_MOVIE_URL_PREFIX + "/" + people_name + "/" + DOU_MOVIE_URL_MIDFIX + str(START_POINT) + DOU_MOVIE_URL_SUFFIX
		START_POINT += STEP_NUM

def extract_movies_elements_with_soup(url):
	print ("extract movies from url: " + url)
	response = requests.get(url).text
	soup = BeautifulSoup(response, "html.parser")
	movies = soup.find_all("div", class_="item")
	return movies

def parse_movie_element_to_list(movie_list, movies):
	print ("parse movies into global list...")
	for movie in movies:
		info = movie.find("div", class_="info")
		name = info.find("li", class_="title").a.em.get_text()
		intro = info.find("li", class_="intro").get_text()
		movie_list.append(Movie(name, intro))
	return movie_list

def dump_movie_list_to_json_file(movie_list):
	with open('movie.json', 'w') as writeJson:
		json.dump(list(map(lambda movie: movie.__dict__, movie_list)), writeJson)

def handler(people_name):
	print ("Start to fetch movies...")
	all_movies_list = []
	url_generator = dou_movie_url_generator(people_name)
	while True:
		movies = extract_movies_elements_with_soup(url_generator.next())
		if movies:
		 	parse_movie_element_to_list(all_movies_list, movies)
		 	time.sleep(20) # here is not a good implentation. Pause 30s. 1. avoid crawler being forbidding. 2. let the http traffic execute. 3. not leverage multi-thread ??
		else:
		 	print ("Guess we hit the wall. end fetching...")
		 	break
	dump_movie_list_to_json_file(all_movies_list)

#It's syn way to fetch watch list. It's very basic way.
def main():
	try:
		targetPeople = sys.argv[1]
		handler(targetPeople)
	except IndexError as e:
		print ("Ah, seem like no target people...?, please look the trace back info below.")
		raise e

if __name__ == '__main__':
	main()