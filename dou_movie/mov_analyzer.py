#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json

def main():
	movies = json.load(open("movie.json"))
	targetMovies = list(filter(lambda movie: u"日本" in movie[u"intro"], movies))
	print len(targetMovies)
	# for item in targetMovies:
	# 	print item[u"name"]
	# 	print "\n"

if __name__ == '__main__':
	main()