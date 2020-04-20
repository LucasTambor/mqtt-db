#!/usr/bin/python3

from mqttHandler import MqttHandler
from persister import SqliteDB
from AzureHubIoT import HubIotHandler
import time

DB_FILE = '/home/root/iotdata.db'
CLOUD_CONN_STR = "HostName=tambor-iot-hub.azure-devices.net;DeviceId=rasp0-tambor-iot;SharedAccessKey=DPNWHr2DWuguf3dB1Ez9YGdP/OFy3HEuFOdrQgrIkcE="

def main():
    #Create Objetcts
    mqttApp = MqttHandler()
    db = SqliteDB(DB_FILE)
    cloud = HubIotHandler(CLOUD_CONN_STR, True)

    db.CreateTable("mqttAppTable")

    mqttApp.subscribe()

    #Add Data Base and Cloud Service to MqttApp
    mqttApp.AddPersister(db)
    # mqttApp.AddCloudService(cloud)

    mqttApp.start()
    mqttApp.Run()

if __name__ == '__main__':
    main()
