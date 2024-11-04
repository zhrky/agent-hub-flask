import json, requests

from datetime import datetime

def get_current_time(data):
    location = data["location"]
    current_time = datetime.now().strftime("%I:%M %p")    
    print(json.dumps({"location": location, "current_time": current_time}))      
    return ({"location": location, "current_time": current_time})
