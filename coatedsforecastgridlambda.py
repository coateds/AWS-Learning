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

    for element in elementlist:
        rtnstring += f"\t\t<td>{element}</td>\n"
    rtnstring += '\t</tr>\n'
    return rtnstring

def tblhdrfromlist(elementlist, style):
    # trstyle = ' style="height: 40px; color: yellow; background-color: #12127d; font-weight: bold; vertical-align: bottom;"'

    rtnstring = ''
    rtnstring += '\t<tr style="height: 40px; color: yellow; background-color: #12127d; font-weight: bold; vertical-align: bottom">\n'

    for element in elementlist:
        rtnstring += f"\t\t<td>{element}</td>\n"
    rtnstring += '\t</tr>\n'
    return rtnstring


def handler(event, context):
    utc_time = datetime.datetime.utcnow()
    pt = utc_time.astimezone(tz)
    timestamp = f"Last Update: {pt.strftime('%H:%M:%S')}"

    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        print("Error: no 'OWM_API_KEY' provided")
        sys.exit(1)
    # else:
        # print(api_key)

    # bothellobj = getforecastobj(47.76, -122.20, api_key)
    ashfordobj = getforecastobj(46.75, -122.03, api_key)
    leavenworthobj = getforecastobj(47.60, -120.66, api_key)

    marblemountobj = getforecastobj(48.53, -121.44, api_key)
    winthropobj = getforecastobj(48.46, -120.18, api_key)
    # indexobj = getforecastobj(47.82, -121.55, api_key)
    northbendobj = getforecastobj(47.50, -121.78, api_key)
    # cleelumobj = getforecastobj(47.20, -120.93, api_key)
    ptangelesobj = getforecastobj(48.11, -123.44, api_key)
    # quilceneobj = getforecastobj(47.82, -122.88, api_key)

    htmlstr = f"<p>{timestamp}</p>\n"
    htmlstr += '<table style="width: 80%;" border="0" cellspacing="0" cellpadding="0">\n'
    htmlstr += tblhdrfromlist(["Today", "Marblemount", "Winthrop", "North Bend", "Leavenworth", "Ashford", "Pt Angeles"], ' style="background-color: #12127d;"')

    count = 0
    while count < marblemountobj['cnt'] - 1:
        utc_time = datetime.datetime.fromtimestamp(marblemountobj['list'][count]['dt'])
        pt = utc_time.astimezone(tz)

        cell1 = pt.strftime('%H:%M:%S')
        cell2 = str(marblemountobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(marblemountobj['list'][count]['main']['temp']), 1)) + "F"
        cell3 = str(winthropobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(winthropobj['list'][count]['main']['temp']), 1)) + "F"
        cell4 = str(northbendobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(northbendobj['list'][count]['main']['temp']), 1)) + "F"
        cell5 = str(leavenworthobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(leavenworthobj['list'][count]['main']['temp']), 1)) + "F"
        cell6 = str(ashfordobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(ashfordobj['list'][count]['main']['temp']), 1)) + "F"
        cell7 = str(ptangelesobj['list'][count]['weather'][0]['description']) + " " + str(round(cFar(ptangelesobj['list'][count]['main']['temp']), 1)) + "F"
        htmlstr += tblrowfromlist([cell1, cell2, cell3, cell4, cell5, cell6, cell7])

        if (str(pt.strftime('%H:%M:%S')).find('23:00') != -1) or (str(pt.strftime('%H:%M:%S')).find('22:00') != -1):
            # strheader = tblrowfromlist(["&nbsp;", "&nbsp;", "&nbsp;", "&nbsp;"])
            # htmlstr += strheader
            strheader = tblhdrfromlist([weekday(marblemountobj['list'][count + 1]['dt']), "Marblemount", "Winthrop", "North Bend", "Leavenworth", "Ashford", "Pt Angeles"], '')
            htmlstr += strheader

        count += 1

    htmlstr += '</table>\n'

    writebuckettextfile('coateds-forecast-grid-web', 'index.html', htmlstr)
