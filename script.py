# import pyodbc
import configparser

import requests
import json
import csv
from datetime import datetime
import uuid

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def fetchData():
    try:
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
        blob_name = f"{today.day}{today.month}{today.year}.csv"

        with open(csv_file, 'w') as fp:
            csv_writer = csv.writer(fp, delimiter='|')
            csv_writer.writerows(earthquakes)

        load(csv_file, blob_name)
        return
    except Exception as ex:
        print('Exception:')
        print(ex)


def load(local_file_name, blob_name):
    try:
        config = configparser.ConfigParser()
        config.read('config.conf')

        connect_str = config['AZURE']['AZURE_STORAGE_CONNECTION_STRING']

        # Create a unique name for the container
        container_name = config['AZURE']["CONTAINER_NAME"]

        # Create a blob client using the local file name as the name for the blob
        blob_client = BlobClient.from_connection_string(
            conn_str=connect_str, container_name=container_name,
            blob_name=blob_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

        # Upload the created file
        with open(file=local_file_name, mode="rb") as data:
            print(data)
            blob_client.upload_blob(data)

    except Exception as ex:
        print('Exception:')
        print(ex)


fetchData()
