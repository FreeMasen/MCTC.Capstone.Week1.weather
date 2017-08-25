import urllib.request as request
from urllib.parse import quote
import json
import io
import os
import datetime
import time

def get_weather(city, country):
    try:
        cache_path = "%s/weather.%s.%s.json" % (os.getcwd(), city, country)
        old_weather = open(cache_path)
        weather = json.load(old_weather)
        old_weather.close()
        last_check = time.time(weather["lastCheck"])
        five_minutes = 60 * 5
        if (time.time - last_check > five_minutes):
            raise ValueError
    except Exception as e:
        raw_weather = request_weather(city, country)
        weather = parse_weather(raw_weather, city, country)
        cache = open(cache_path, 'w')
        cache.write(json.dumps(weather))
    return weather

def request_weather(city, country):
    baseUrl = "https://api.openweathermap.org/data/2.5/weather?"
    api_key = get_api_key()
    fullUrl = "%sq=%s,%s&APPID=%s" % (baseUrl, city, country, api_key)
    try:
        res = request.urlopen(fullUrl)
    except Exception as e:
        print("Sorry, there was an error getting the response")
        print(e)
        return

    try: 
        body = res.read()
        return json.loads(body.decode('utf-8'))
    except Exception as e:
        print(e)
        print("There was an error parsing the response")

def get_api_key():
    try:
        raw_settings = open('%s/settings.json' % os.getcwd())
        settings = json.load(raw_settings)
        return settings['api_key']
    except Exception as e:
        print("Sorry, there was an error getting the api key")
        print(e)

def parse_weather(weather, city, country):
    return {"sky": weather["weather"][0]["description"],
            "humidity": weather["main"]["humidity"],
            "pressure": weather["main"]["pressure"],
            "wind": calculate_wind(weather["wind"]["speed"], weather["wind"]["deg"]),
            "high":weather["main"]["temp_max"],
            "low": weather["main"]["temp_min"],
            "current": weather["main"]["temp"],
            "sunrise": weather["sys"]["sunrise"],
            "sunset": weather["sys"]["sunset"],
            "city": city[0].upper() + city[1:],
            "country": country.upper(),
            "lastCheck": time.time()}

def calculate_wind(speed, direction):
    if (direction > 338 and direction < 22):
        dirString = "N"
    elif (direction > 22 and direction < 67):
        dirString = "NE"
    elif (direction > 67 and direction < 112):
        dirString = "E"
    elif (direction > 112 and direction < 157):
        dirString = "SE"
    elif (direction > 157 and direction < 202):
        dirString = "S"
    elif (direction > 202 and direction < 247):
        dirString = "SW"
    elif (direction > 247 and direction < 292):
        dirString = "W"
    else:
        dirString = "NW"
    return "%s m/s %s" % (speed, dirString)
        

def displayWeather(weather):
    print("%s (%s)\n" % (weather["city"], weather["country"]))
    print("------------------------------\n")
    print("Conditions:\n")
    print("==============================\n")
    print("Sky %s\n" % (weather["sky"]))
    print("Humidity %s\n" % (weather["humidity"]))
    print("Pressure %s" % (weather["pressure"]))
    print("Wind %s" % (weather["wind"]))
    print("\n")
    print("Temperature:\n")
    print("==============================\n")
    print("High %s\n" % (weather["high"]))
    print("Low %s" % (weather["low"]))
    print("Current %s\n" % (weather["current"]))
    print("\n")
    print("Light:\n")
    print("==============================\n")
    print("Sunrise %s\n" % (weather["sunrise"]))
    print("Sunset %s\n" % (weather["sunset"]))

def main():
    weather = get_weather("minneapolis", "usa")
    displayWeather(weather)

main()