const weatherUrl = "https://api.open-meteo.com/v1/forecast?latitude=18.11&longitude=-65.86&hourly=temperature_2m,rain,precipitation_probability,apparent_temperature,dew_point_2m,relative_humidity_2m&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,weather_code,wind_speed_10m,cloud_cover,pressure_msl,surface_pressure&timezone=auto&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch";

fetch(weatherUrl)
  .then((res) => res.json())
  .then((data) => {
    
    //Extract correct current values
    const temperature = data.current.temperature_2m;
    const windSpeed = data.current.wind_speed_10m;
    const time = data.current.time;

    //Safely get current hour for hourly precipitation probability
    const currentHourIndex = data.hourly.time.indexOf(time);
    const precipProbability = data.hourly.precipitation_probability[currentHourIndex];

    //Update DOM
    document.getElementById("temperature").textContent = temperature;
    document.getElementById("wind").textContent = windSpeed;
    document.getElementById("precipitation_probability").textContent = precipProbability;
    document.getElementById("time").textContent = time;
  })
  .catch((error) => {
    console.error("Error fetching weather data:", error);
  });