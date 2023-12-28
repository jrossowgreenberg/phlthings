import openmeteo_requests
import pandas as pd


class PhlWthrModel:
    def __init__(self):
        self.openmeteo = openmeteo_requests.Client()

    def get_forecast(self):
        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 39.9523,
            "longitude": -75.1638,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "sunrise",
                "sunset",
                "daylight_duration",
                "precipitation_sum",
            ],
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "America/New_York",
        }
        responses = self.openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_sunrise = daily.Variables(2).ValuesInt64AsNumpy()
        daily_sunset = daily.Variables(3).ValuesInt64AsNumpy()
        daily_daylight_duration = daily.Variables(4).ValuesAsNumpy() / 60 / 60
        daily_precipitation_sum = daily.Variables(5).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s"),
                end=pd.to_datetime(daily.TimeEnd(), unit="s"),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left",
            )
        }
        daily_data["date"] = pd.to_datetime(daily_data["date"]).date
        daily_data["temp_high"] = daily_temperature_2m_max
        daily_data["temp_low"] = daily_temperature_2m_min
        # daily_data["sunrise"] = daily_sunrise
        daily_data["sunrise"] = (
            pd.to_datetime(daily_sunrise, unit="s", utc=True)
            .tz_convert("America/New_York")
            .strftime("%H:%M:%S")
        )

        daily_data["sunset"] = (
            pd.to_datetime(daily_sunset, unit="s", utc=True)
            .tz_convert("America/New_York")
            .strftime("%H:%M:%S")
        )
        daily_data["daylight_duration"] = daily_daylight_duration
        daily_data["precip"] = daily_precipitation_sum

        daily_dataframe = pd.DataFrame(data=daily_data)
        return daily_dataframe.to_dict()
