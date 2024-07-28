from datetime import datetime

night_weather_codes = ["1220", "1250"]

def get_hourly_weather_icon(hour, weather_code, strptime="%H:%M"):
    hourly_weather_code = weather_code
    time_object = datetime.strptime(hour, strptime)
    if _is_night(time_object.hour) and hourly_weather_code in night_weather_codes:
        hourly_weather_code = hourly_weather_code + "-night"

    return hourly_weather_code

def _is_night(hour):
    return hour < 6 or hour > 20