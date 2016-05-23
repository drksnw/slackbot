"""Prototype for Weathercast Bot"""

from config import OWA_TOKEN
import requests
import json

def get_forecast(city_name, country):
    url = "http://api.openweathermap.org/data/2.5/weather?q="+city_name+","+country+"&appid="+OWA_TOKEN
    response = requests.get(url)
    jdata = json.loads(response.text)
    temp = jdata["main"]["temp"]
    temp -= 273.15 # Temperature given is in Kelvin...
    wea = jdata["weather"][0]["main"]
    wea_desc = jdata["weather"][0]["description"]
    print("Weather forecast for "+city_name+", "+country+"\n"+wea+" : "+wea_desc+"\nTemp: "+str(temp)+"°C")
