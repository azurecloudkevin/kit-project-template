omni.kit.pipapi.install("paho")
omni.kit.pipapi.install("random")
omni.kit.pipapi.install("json")
omni.kit.pipapi.install("os")
omni.kit.pipapi.install("csv")
import csv
from .robotmotion import RobotMotion
from paho import client as mqtt_client
import random
import json
import time
import os

class MQTTData:
    def __init__(self):
        self.topic = str(os.environ['MQTT_TOPIC']) 
        self.client = self.connect_mqtt(self.topic)

    def read_csv(self, file_name):
        data = {}

        with open(file_name, 'r', encoding='UTF-8') as file:
            while line := file.readline():
                coordinatearray = ["x", "y", "z", "o", "a", "t"]
                counter = 0
                lines = line.rstrip()
                for coord in lines:

                    if coord.isnumeric():
                        data[coordinatearray[counter]] = coord
                    else:
                        break
                    counter = counter + 1

                json_data = json.dumps(data, indent=2).encode("utf-8")
                        
                self.write_to_mqtt(self.client, self.topic, json_data)


    # publish to mqtt broker
    def write_to_mqtt(mqtt_client, topic, data, ts):
        mqtt_client.publish(topic, data)


    # connect to mqtt broker
    def connect_mqtt(topic):

        # called when a message arrives
        def on_message(client, userdata, msg):
            msg_content = msg.payload.decode()
            coords = json.loads(msg_content)
            coordinatearray = []
            coordinatearray.append(coords["x"])
            coordinatearray.append(coords["y"])
            coordinatearray.append(coords["z"])
            coordinatearray.append(coords["o"])
            coordinatearray.append(coords["a"])
            coordinatearray.append(coords["t"])
            RobotMotion.next_pose(coordinatearray)

            print(f"Received `{msg_content}` from `{msg.topic}` topic")

        # called when connection to mqtt broker has been established
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                # connect to our topic
                print(f"Subscribing to topic: {topic}")
                client.subscribe(topic)
            else:
                print(f"Failed to connect, return code {rc}")

        # let us know when we've subscribed
        def on_subscribe(client, userdata, mid, granted_qos):
            print(f"subscribed {mid} {granted_qos}")

        # Set Connecting Client ID
        client = mqtt_client.Client(f"python-mqtt-{random.randint(0, 1000)}")

        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe
        client.username_pw_set(username='client2-authn-ID')
        #ctx = _ssl.SSLContext()
        #ctx.load_cert_chain(certfile='C:\\Users\\Hub1\\client1-authn-ID.pem',keyfile='C:\\Users\\Hub1\\client1-authn-ID.key')
        #client.tls_set_context(context=ctx)
        #client.tls_insecure_set(True)
        client.tls_set()
        #certfile='C:\\Workspaces\\iot-samples\\source\\ingest_app_mqtt\\client2-authn-ID.pem',
        #keyfile='C:\\Workspaces\\iot-samples\\source\\ingest_app_mqtt\\client2-authn-ID.key'

        result = client.connect("simulated-plant-eg.eastus-1.ts.eventgrid.azure.net", 8883)
        client.loop_start()
        return client
