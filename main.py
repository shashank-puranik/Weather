import logging
import datetime as dt
import config
import pandas as pd
import urllib.request
import json

from pandas import json_normalize

apikey = open('api_key','r').read()

def extractWeatherData(url):
    response_site = urllib.request.urlopen(url)
    try:
        print("Connecting to URL:", url)
        utf8_data = response_site.read()
        print("URL connected successfully.")
    except Exception as exn:
        logging.error("The error is {} : {}".format(exn.__class__.__name__, exn))

    json_obj = json.loads(utf8_data.decode("utf-8"))
    print("Data retrieved successfully.")
    return json_obj['SiteRep']['DV']['Location']

def extractSiteData(url):
    response_sites = urllib.request.urlopen(url)
    try:
        print("Connecting to URL:", url)
        utf8_dataa = response_sites.read()
        print("URL connected successfully.")
    except Exception as exn:
        logging.error("The error is {} : {}".format(exn.__class__.__name__, exn))

    json_object = json.loads(utf8_dataa.decode("utf-8"))
    return json_object['SiteRep']['DV']

def normaliseaspandasdf(json_obj, location_key=config.locationkeys()):
    return json_normalize(json_obj, record_path=["Period", "Rep"], meta=location_key)


def extractweatherdatadaily(pandasdf):
    logging.info("Extracting the daily weather data.")
    renamed_df = pandasdf.rename(columns=config.dailydatacolumnsmapping())
    renamed_df["weather_date"] = pd.to_datetime(renamed_df["weather_date"], format="%Y-%m-%dZ")
    renamed_df = renamed_df.fillna(0)
    renamed_df.loc[:, config.dailydatacolconvert()] = renamed_df.loc[:, config.dailydatacolconvert()].apply(pd.to_numeric)
    return renamed_df

def main():
    # Set up the URL for daily weather data
    #urldaily = config.url()
    sites = config.url()
    # Call the extractWeatherData function and get the weather data
    #weather_data = extractWeatherData(urldaily)
    site_info = extractSiteData(sites)
    # Print the weather_data
    #normalised_daily = normaliseaspandasdf(weather_data)
    #dailyweatherdata = extractweatherdatadaily(normalised_daily)
    #dailyweatherdata.to_csv("DailyWeatherData_{}.csv".format(dt.datetime.today().strftime('%Y-%m-%d')), header=True, index=False, encoding='utf-8')
    df = pd.DataFrame(site_info)
    print(df)
if __name__ == '__main__':
    main()
