from datetime import datetime


def get_hourly_weather_icon(hour, weather_code, strptime="%H:%M"):
    hourly_weather_code = weather_code
    time_object = datetime.strptime(hour, strptime)
    if (time_object.hour < 6 or time_object.hour > 20) and hourly_weather_code == "1250":
        hourly_weather_code = "1250-night"

    return hourly_weather_code
