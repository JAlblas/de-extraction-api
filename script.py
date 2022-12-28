# import pyodbc
import configparser

import requests
import json
import csv
from datetime import datetime

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


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
                current_earthquake.append(feature['properties']['ids'])
                current_earthquake.append(feature['properties']['title'])
                current_earthquake.append(feature['properties']['time'])
                current_earthquake.append(feature['properties']['url'])
                current_earthquake.append(feature['properties']['mag'])
                current_earthquake.append(
                    feature['geometry']['coordinates'][0])
                current_earthquake.append(
                    feature['geometry']['coordinates'][1])

                all_earthquakes.append(current_earthquake)

            write_to_csv(all_earthquakes)

        else:
            print('An error has occurred.')
    except:
        print('A error occured!')


def write_to_csv(earthquakes):
    try:
        today = datetime.now()
        csv_file = f"./data/earthquakes-{today.day}{today.month}{today.year}.csv"

        with open(csv_file, 'w') as fp:
            csv_writer = csv.writer(fp, delimiter='|')
            csv_writer.writerows(earthquakes)
        return
    except Exception as ex:
        print('Exception:')
        print(ex)


def load():
    try:
        print("Azure Blob Storage Python quickstart sample")

    # Quickstart code goes here

    except Exception as ex:
        print('Exception:')
        print(ex)


fetchData()
