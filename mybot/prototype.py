"""Prototype for Weathercast Bot"""

from config import OWA_TOKEN
import requests
import json

def get_forecast(city_name, country):
    url = "http://api.openweathermap.org/data/2.5/weather?q="+city_name+","+country+"&appid="+OWA_TOKEN
    response = requests.get(url)
    jdata = json.loads(response.text)
    if jdata["cod"] == "404":
        return "City not found :cry:"
    temp = jdata["main"]["temp"]
    temp -= 273.15 # Temperature given is in Kelvin...
    wea = jdata["weather"][0]["main"]
    wea_sm = ":question:"
    if wea == "Clouds":
        wea_sm = ":cloud:"
    elif wea == "Rain":
        wea_sm = ":rain_cloud:"
    elif wea == "Clear":
        wea_sm = ":sun_with_face:"
    wea_desc = jdata["weather"][0]["description"]
    return "Weather forecast for "+jdata["name"]+", "+jdata["sys"]["country"]+"\n"+wea+" "+wea_sm+" : "+wea_desc+"\nTemp: "+str(temp)+"°C"
