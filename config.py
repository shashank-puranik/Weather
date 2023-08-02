def urls():
    urldaily = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/all?res=daily&key={}"
    return urldaily

def dailydatacolumnsmapping():
    return {
        'i': 'siteid',
        'lat': 'latitude',
        'Dm': 'day_max_temperature',
        'Period.value': 'weather_date',
        'FDm': 'feels_like_day_max_temperature',
        'Gn': 'wind_gust_noon',
        'U': 'max_uv_index',
        'name': 'region',
        'Hn': 'screen_relative_humidity_noon',
        'PPd': 'precipitation_probability_day',
        'lon': 'longitude',
        'D': 'wind_direction',
        'Gm': 'wind_gust_midnight',
        'Hm': 'screen_relative_humidity_midnight',
        'PPn': 'precipitation_probability_night',
        'S': 'wind_speed',
        'V': 'visibility',
        'Nm': 'night_min_temperature',
        'FNm': 'feels_like_night_min_temperature',
        'W': 'weather_type',
        'max_uv_index': '0',
        '$': 'daynight_indicator',
    }

def dailydatacolconvert():
    return ['day_max_temperature',
            'feels_like_day_max_temperature',
            'feels_like_night_min_temperature',
            'wind_gust_midnight',
            'wind_gust_noon',
            'screen_relative_humidity_midnight',
            'screen_relative_humidity_noon',
            'night_min_temperature',
            'precipitation_probability_day',
            'wind_speed',
            'max_uv_index',
            'weather_type',
            'longitude',
            'latitude',
            'siteid',
            'precipitation_probability_night']

def addnewcolumns():
    return ['dl_filename',
            'dl_line_no',
            'dl_file_date',
            'dl_insert_dttm',
            'dl_talend_job_id',
            'dl_talend_job_run_id']

