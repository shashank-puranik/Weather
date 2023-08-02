import logging
import datetime as dt
import config

import urllib
import json

apikey = open('api-key.txt','r').read()

def extractWeatherData(url):
    response_site = urllib.request.urlopen(url+apikey)
    try:
        print("Connecting to URL:", url)
        utf8_data = response_site.read()
        print("URL connected successfully.")
    except Exception as exn:
        logging.error("The error is {} : {}".format(exn.__class__.__name__, exn))

    json_obj = json.loads(utf8_data, encoding="utf-8")
    print("Data retrieved successfully.")
    return json_obj['SiteRep']['DV']['Location']

def main():
    # Set up the URL for daily weather data
    urldaily = config.urls()

    # Call the extractWeatherData function and get the weather data
    weather_data = extractWeatherData(urldaily)

    # Print the weather_data
    print(weather_data)

if __name__ == '__main__':
    main()
