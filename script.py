#import pyodbc

config = configparser.ConfigParser()
config.read('config.conf')

print(config['DEFAULT']['url'])


url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'

response = requests.get(url)

if response:
    json = response.json()
    features = json['features']

    for feature in features:
        print(feature)
        print("==================================")

else:
    print('An error has occurred.')


