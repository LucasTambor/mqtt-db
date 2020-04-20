#!/usr/bin/python3
import uuid
from azure.iot.device import IoTHubDeviceClient, Message


class HubIotHandler(object):
    DEBUG = False
    CLOUD_SERVICE_NAME = "Azure Hub IoT"
    CONN_STR = ""

    def __init__(self, conn_str, debug=False):
        self.DEBUG = debug

        if self.DEBUG:
            print("Creating Hub Iot Handler")
            print("Connection string: {}".format(conn_str))
        self.CONN_STR = conn_str

    def sendMessage(self, msg):
        if self.DEBUG:
            print("Sending Message to Hub IoT: {}".format(msg))
        device_client = IoTHubDeviceClient.create_from_connection_string(self.CONN_STR)
        device_client.connect()
        msg = Message(msg)
        msg.message_id =  uuid.uuid4()
        device_client.send_message(msg)
        device_client.disconnect()
