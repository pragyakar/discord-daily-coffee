import requests 
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re


def getHoroscope(zodiac):    
    url = 'http://sandipbgt.com/theastrologer/api/horoscope/'+zodiac+'/today/'
    h = requests.get(url)
    h = h.json()
    return h['sunsign'], h['date'], h['horoscope'], h['meta']['mood'], h['meta']['keywords'], h['meta']['intensity']

def getJoke():
    url = 'http://api.yomomma.info/'
    j = requests.get(url)
    j = j.json()
    return j['joke']

def getMovies():
    now_showing = []
    comming_soon =  []

    try:
        html = urlopen('http://qfx.com.np/Home/Index')
    except HttpError as error:
        print(error)
    except URLError:
        print('Possible server issue')
    else:
        soup = BeautifulSoup(html.read(), 'html5lib')
        tags = soup.findAll('div', {'class': 'movie'})
        for tag in tags:
            movie_name = tag.find('h4', {'class': 'movie-title'}) 
            date = tag.find('p', {'class': 'movie-date'})   
                
            if (date == None):
                now_showing.append(movie_name.getText())
            else:
                comming_soon.append(movie_name.getText())
    return now_showing, comming_soon


    

