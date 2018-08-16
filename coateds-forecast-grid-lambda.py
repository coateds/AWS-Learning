import requests
import os
import sys
import datetime
import boto3
from io import StringIO

s3 = boto3.client('s3')

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

def writebuckettextfile(bucket, file, contents):
    # Write to a file
    # notice if you do fake_handle.read() it reads like a file handle
    fake_handle = StringIO(contents)
    s3.put_object(Bucket=bucket, Key=file, Body=fake_handle.read(), ContentType='text/html', ContentEncoding='utf-8')

def getforecastobj(lat, lon, key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}"
    res = requests.get(url)
    return res.json()

def tblrowfromlist(elementlist):
    rtnstring = ''
    rtnstring += '\t<tr>\n'

    # firstheader = ["Today", "Bothell", "Ashford", "Leavenworth"]
    for element in elementlist:
        rtnstring += f"\t\t<td>{element}</td>\n"
    rtnstring += '\t</tr>\n'
    return rtnstring

def lambda_handler(event, context):
    # Get the api key from environment variables
    # will want another method at some point
    api_key = os.getenv("OWM_API_KEY")

    if not api_key:
        print("Error: no 'OWM_API_KEY' provided")
        sys.exit(1)
    # else:
        # print(api_key)
    
    bothellobj = getforecastobj(47.76, -122.20, api_key)
    ashfordobj = getforecastobj(46.75, -122.03, api_key)
    leavenworthobj = getforecastobj(47.60, -120.66, api_key)

    htmlstr = '<table>\n'

    strheader = tblrowfromlist(["Today", "Bothell", "Ashford", "Leavenworth"])
    htmlstr += strheader

    count = 0
    while count < bothellobj['cnt'] - 1:
        cell1 = twentyfourhrtime(bothellobj['list'][count]['dt'])
        cell2 = str(bothellobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(bothellobj['list'][count]['main']['temp']), 1)) + "F"
        cell3 = str(ashfordobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(ashfordobj['list'][count]['main']['temp']), 1)) + "F"
        cell4 = str(leavenworthobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(leavenworthobj['list'][count]['main']['temp']), 1)) + "F"
        strheader = tblrowfromlist([cell1, cell2, cell3, cell4])
        htmlstr += strheader

        if str(fulldate(bothellobj['list'][count]['dt'])).find('23:00') != -1:
            strheader = tblrowfromlist(["&nbsp;", "&nbsp;", "&nbsp;", "&nbsp;"])
            htmlstr += strheader
            strheader = tblrowfromlist([weekday(bothellobj['list'][count + 1]['dt']), "Bothell", "Ashford", "Leavenworth"])
            htmlstr += strheader
        
        count += 1

    htmlstr += '</table>\n'

    writebuckettextfile('coateds-forecast-grid-web', 'index.html', htmlstr)