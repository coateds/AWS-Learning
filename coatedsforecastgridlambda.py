import requests
import os
import sys
import datetime
import boto3
from io import StringIO
import pytz
from pytz import all_timezones_set, common_timezones_set

s3 = boto3.client('s3')

tz = pytz.timezone('US/Pacific')

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

# def timeFmt(timeEntry):
#    inputTime = parse(timeEntry).replace(
#                tzinfo=pytz.timezone("UTC")
#    )
#    convTime = inputTime.astimezone(pytz.timezone("US/Pacific"))
#    return convTime

def handler(event, context):
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
        utc_time = datetime.datetime.fromtimestamp(bothellobj['list'][count]['dt'])
        pt = utc_time.astimezone(tz)
        # print(pt.strftime('%H:%M:%S'))
        # inputTime = parse(timeEntry).replace(tzinfo=pytz.timezone("UTC")
        # print(inputTime.astimezone(pytz.timezone("US/Pacific")))
        # print(twentyfourhrtime(datetime.datetime.fromtimestamp(pt)).astimezone(pacific))
        # cell1 = twentyfourhrtime(bothellobj['list'][count]['dt'])
        cell1 = pt.strftime('%H:%M:%S')
        cell2 = str(bothellobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(bothellobj['list'][count]['main']['temp']), 1)) + "F"
        cell3 = str(ashfordobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(ashfordobj['list'][count]['main']['temp']), 1)) + "F"
        cell4 = str(leavenworthobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(leavenworthobj['list'][count]['main']['temp']), 1)) + "F"
        strheader = tblrowfromlist([cell1, cell2, cell3, cell4])
        htmlstr += strheader

        # if str(pt.strftime('%H:%M:%S')).find('23:00') != -1:
        if (str(pt.strftime('%H:%M:%S')).find('23:00') != -1) or (if str(pt.strftime('%H:%M:%S')).find('22:00') != -1):
            strheader = tblrowfromlist(["&nbsp;", "&nbsp;", "&nbsp;", "&nbsp;"])
            htmlstr += strheader
            strheader = tblrowfromlist([weekday(bothellobj['list'][count + 1]['dt']), "Bothell", "Ashford", "Leavenworth"])
            htmlstr += strheader
        
        count += 1

    htmlstr += '</table>\n'htmlstr += '</table>\n'

    writebuckettextfile('coateds-forecast-grid-web', 'index.html', htmlstr)
