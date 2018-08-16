import requests
import os
import sys
import datetime

def fulldate(dt):
    return datetime.datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S')

def twentyfourhrtime(dt):
    return datetime.datetime.fromtimestamp(dt).strftime('%H:%M:%S')

def weekday(dt):
    return datetime.datetime.fromtimestamp(dt).strftime("%A")

# Convert kelvin to celsius
def cCel(k):
    return k - 273.15

def cFar(k):
    return 1.8 * (k - 273) + 32

def getforecastobj(lat, lon, key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}"
    res = requests.get(url)
    return res.json()

def handler(event, context):
    print('anything')

    api_key = os.getenv("OWM_API_KEY")
    bothellobj = getforecastobj(47.76, -122.20, api_key)
    print('Bothell immediate forecast is')
    print(str(bothellobj['list'][0]['weather'][0]['description']))
    print(str(round(cFar(bothellobj['list'][0]['main']['temp']), 1)) + "F")