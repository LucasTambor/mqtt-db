#!/usr/bin/python3

from mqttHandler import MqttHandler
from persister import SqliteDB
import time

DB_FILE = '/home/root/iotdata.db'


def main():
    mqttApp = MqttHandler()
    db = SqliteDB(DB_FILE)
    db.CreateTable("mqttAppTable")
    mqttApp.subscribe()
    mqttApp.AddPersister(db)
    
    mqttApp.start()
    mqttApp.Run()

if __name__ == '__main__':
    main()
