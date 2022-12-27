# import pyodbc
import configparser

import requests
import json
import csv


def fetchData():
    try:
        config = configparser.ConfigParser()
        config.read('config.conf')

        # print(config['DEFAULT']['url'])

        url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'

        response = requests.get(url)

        if response:
            json = response.json()
            features = json['features']
            all_earthquakes = []

            for feature in features:
                current_earthquake = []
                print(feature)
                print("==================================")
                current_earthquake.append(feature['properties']['mag'])
                current_earthquake.append(
                    feature['geometry']['coordinates'][0])
                current_earthquake.append(
                    feature['geometry']['coordinates'][1])

                all_earthquakes.append(current_earthquake)

            csv_file = 'earthquakes.csv'

            with open(csv_file, 'w') as fp:
                csv_writer = csv.writer(fp, delimiter='|')
                csv_writer.writerows(all_earthquakes)
        else:
            print('An error has occurred.')
    except:
        print('A error occured!')


fetchData()
