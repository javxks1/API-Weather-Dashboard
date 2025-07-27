import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

#Open-Meteo API client
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 18.11,
	"longitude": -65.86,
	"hourly": ["temperature_2m", "rain", "precipitation_probability", "apparent_temperature", "dew_point_2m", "relative_humidity_2m"],
	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "weather_code", "wind_speed_10m", "cloud_cover", "pressure_msl", "surface_pressure"],
	"timezone": "auto",
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values  
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_apparent_temperature = current.Variables(2).Value()
current_is_day = current.Variables(3).Value()
current_precipitation = current.Variables(4).Value()
current_rain = current.Variables(5).Value()
current_weather_code = current.Variables(6).Value()
current_wind_speed_10m = current.Variables(7).Value()
current_cloud_cover = current.Variables(8).Value()
current_pressure_msl = current.Variables(9).Value()
current_surface_pressure = current.Variables(10).Value()

print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
print(f"Current apparent_temperature {current_apparent_temperature}")
print(f"Current is_day {current_is_day}")
print(f"Current precipitation {current_precipitation}")
print(f"Current rain {current_rain}")
print(f"Current weather_code {current_weather_code}")
print(f"Current wind_speed_10m {current_wind_speed_10m}")
print(f"Current cloud_cover {current_cloud_cover}")
print(f"Current pressure_msl {current_pressure_msl}")
print(f"Current surface_pressure {current_surface_pressure}")

#Process hourly data
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_rain = hourly.Variables(1).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(2).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(4).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(5).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["rain"] = hourly_rain
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)