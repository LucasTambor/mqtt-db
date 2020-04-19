#!/usr/bin/python3
import time
import paho.mqtt.client as mqtt
import json

class MqttHandler(object):
    mqtt_broker_priv = "127.0.0.1"
    mqtt_broker_pub = "test.mosquitto.org"
    mqtt_port = 1883
    mqtt_keep_alive = 60

    CLIENT_ID = "tamborIoT"

    #Topicos
    TOPIC_1 = "esquenta/iot/unisal"
    MQTT_TOPIC_DATA = "esquenta/iot/unisal/data" #Topic for data send/recv
    MQTT_TOPIC_CMD = "esquenta/iot/unisal/cmd"   #Topic for commands send/recv

    #DB
    has_db = False

    def __init__(self):
        self.client = mqtt.Client(self.CLIENT_ID) #Cria ID unica, broker bloqueia demais acessos com mesma ID
        self.client.on_message = self.on_message # Register callback
        print("Connecting to broker at {}".format(self.mqtt_broker_priv))
        self.client.connect(self.mqtt_broker_priv, self.mqtt_port, self.mqtt_keep_alive)

    def start(self):
        self.client.loop_start() # Start message monitor thread

    def subscribe(self, topic=""):
        #TODO Add list to subscribe and method to add topics
        self.client.subscribe(self.MQTT_TOPIC_DATA)

    #Callbacks
    def on_message(self, client, userdata, message):
        print("#########################################")
        print("Message Received: {}".format(message.payload.decode("utf-8")))
        print("Message Topic: {}".format(message.topic))
        print("Message QoS: {}".format(message.qos))

        if message.topic == self.MQTT_TOPIC_DATA:
            msgRecv = message.payload.decode("utf-8")
            jsonRecv = json.loads(msgRecv)
            status_cmd = False

            if float(jsonRecv["HUMID"]) > 70.0:
                status_cmd = True

            command = {
                "ID": self.CLIENT_ID,
                "CMD": status_cmd,
            }

            print(json.dumps(command))
            client.publish(self.MQTT_TOPIC_CMD, json.dumps(command))

            if(self.has_db):
                self.saveJsonToDb(jsonRecv)


    def AddPersister(self, db):
        self.db = db
        self.has_db = True
        print("Adding DB to MqttHandler: {}".format(self.db.DB_NAME))

    def saveJsonToDb(self, json):
        print("Saving data to db {}".format(self.db.DB_NAME))
        self.db.saveJson(json)
        # self.db.PrintTable()

    def Run(self):
        while 1:
            time.sleep(1)
