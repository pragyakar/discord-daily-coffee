import requests 

def getHoroscope(zodiac):    
    url = 'http://sandipbgt.com/theastrologer/api/horoscope/'+zodiac+'/today/'
    r = requests.get(url)
    r = r.json()
    return r['sunsign'], r['date'], r['horoscope'], r['meta']['mood'], r['meta']['keywords'], r['meta']['intensity']

def getJoke():
    url = 'http://api.yomomma.info/'
    r = requests.get(url)
    r = r.json()
    return r['joke']
