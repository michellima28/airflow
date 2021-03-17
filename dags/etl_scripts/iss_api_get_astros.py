import requests
import json
import pandas as pd
import datetime as dt

# Function that creates a formatted string of the Python JSON object
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Get data from ISS API
response = requests.get("http://api.open-notify.org/astros.json")
data = response.json()
df = pd.json_normalize(data['people'])
df['index'] = range(1, len(df)+1)
df['snapshot_date'] = dt.datetime.now()
df = df[['index', 'snapshot_date', 'craft', 'name']]
