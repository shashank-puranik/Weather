import logging
import datetime as dt
import config
import pandas as pd
import urllib.request
from urllib.error import HTTPError   
from datetime import date


import json

from pandas import json_normalize

apikey = open('api_key','r').read()

def extractWeatherData(url):
    response_site = urllib.request.urlopen(url)
    try:
        print("Connecting to URL:", url)
        utf8_data = response_site.read()
        print("URL connected successfully.")
    except HTTPError as e:
        content = e.read()

    json_obj = json.loads(utf8_data.decode("utf-8"))
    print("Data retrieved successfully.")
    return json_obj['SiteRep']['DV']['Location']

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
    urldaily = config.url()
    # Call the extractWeatherData function and get the weather data
    weather_data = extractWeatherData(urldaily)
    # Print the weather_data
    normalised_daily = normaliseaspandasdf(weather_data)
    dailyweatherdata = extractweatherdatadaily(normalised_daily)
    #dailyweatherdata.to_csv("DailyWeatherData_{}.csv".format(dt.datetime.today().strftime('%Y-%m-%d')), header=True, index=False, encoding='utf-8')
    df = pd.DataFrame(dailyweatherdata)
    print(df)
    today_date = date.today()
    today_date = pd.Timestamp(today_date)
    df['weather_date'] = pd.to_datetime(df['weather_date'], format='%Y/%m/%d')
    print(df.dtypes)
    df_filtered = df[df.apply(lambda x: x["weather_date"] == today_date, axis=1)]
    print(df_filtered)
    df_day = df_filtered[df_filtered.apply(lambda x: x['daynight_indicator'] == 'Day',axis=1)]
    df_night = df_filtered[df_filtered.apply(lambda x:x['daynight_indicator'] == 'Night',axis=1)]
    df_day = df_day.drop(columns=['wind_direction', 'wind_gust_noon','screen_relative_humidity_noon','wind_speed', 'visibility','feels_like_day_max_temperature', 'max_uv_index','wind_gust_midnight','screen_relative_humidity_midnight','precipitation_probability_night', 'night_min_temperature','feels_like_night_min_temperature','latitude', 'longitude','siteid'],axis=1)
    df_night = df_night.drop(columns=['wind_direction', 'wind_gust_noon', 'screen_relative_humidity_noon', 'precipitation_probability_day','wind_speed', 'visibility', 'day_max_temperature', 'feels_like_day_max_temperature','max_uv_index', 'wind_gust_midnight', 'screen_relative_humidity_midnight', 'feels_like_night_min_temperature','latitude','longitude', 'siteid'],axis=1)
    df_day = df_day.rename(columns={'weather_type':'day_weather_type'})
    df_night = df_night.rename(columns={'weather_type':'night_weather_type'})
    df_final = pd.merge(df_day,df_night, on='region',how='inner')
    df_final = df_final.drop(columns=['daynight_indicator_x','daynight_indicator_y','weather_date_y'])
    df_final = df_final.rename(columns={'weather_date_x':'weather_date','day_weather_type':'Value'})
    url_weather_type = "https://raw.githubusercontent.com/shashank-puranik/Weather/main/data.csv"
    weather_type = pd.read_csv(url_weather_type, index_col=0)
    df_final = pd.merge(df_final,weather_type,left_on="day_weather_type",right_on="Value",how="inner")
    df_final = pd.merge(df_final,weather_type,left_on="night_weather_type",right_on="Value",how="inner")
    print(df_final)
if __name__ == '__main__':
    main()
