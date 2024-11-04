import json, requests

from datetime import datetime

def get_current_datetime(data):
    location = data["location"]
    current_datetime = datetime.now().strftime("%Y-%m-%d %I:%M %p")  
    return ({"location": location, "current_datetime": current_datetime})

def get_current_weather(data):
    try:
        location = data["location"]
        api_key = "qfzdF6vcjF1Mbhg" + "hpyJDOVvPp8u0aDpf"
        accuwather_location_endpoint = "http://dataservice.accuweather.com/locations/v1/cities/search"
        accuwather_location_url = accuwather_location_endpoint + "?apikey=" + api_key+ "&q=" + location
        locationkey = requests.get(accuwather_location_url).json()[0]["Key"]
        print(locationkey)
        accuwather_api_endpoint = "http://dataservice.accuweather.com/currentconditions/v1/"
        accuwather_api_url = accuwather_api_endpoint + locationkey + "?apikey=" + api_key
        response = requests.get(accuwather_api_url)
        current_weather = response.json()
        print(current_weather)
    except:
        current_weather = "Data not available. API Error"
    return ({"location": location, "current_weather": current_weather})
