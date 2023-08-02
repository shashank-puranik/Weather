import urllib
import json
import datetime as dt
import requests
import sys
import logging

apikey = open('api-key.txt','r').read()

def extractWeatherData(url):
    response_site = urllib.urlopen(url+apikey)
    try:
        utf8_data = response_site.read()
        logging.info("URL connected successfully.")
    except Exception as exn:
        logging.error("The error is {} : {}".format(exn.__class__.__name__, exn))

    json_obj = json.loads(utf8_data, encoding="utf-8")
    return json_obj['SiteRep']['DV']['Location']