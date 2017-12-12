#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from bs4 import BeautifulSoup
import requests
r = requests.get("https://movie.douban.com/people/58293092/collect?start=10&sort=time&rating=all&filter=all&mode=grid").text
soup = BeautifulSoup(r, "html.parser")
print type(soup)
movies = soup.find_all("div", class_="item")
print type(movies)
firstMovie = movies[0]
print type(firstMovie)
info = firstMovie.find("div", class_="info")
title = info.find("li", class_="title")
print title.a.em.get_text()
# intro = info.find("li", class_="intro")
# targetStr = u'中国大陆'
# if (targetStr in intro.get_text()):
# 	print "this is a china mainland movie"
# else:
# 	print "it may not be screen in mainland china"

