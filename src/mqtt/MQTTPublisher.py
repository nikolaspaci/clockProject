import paho.mqtt.client as mqtt
import os
import json
from dotenv import load_dotenv

load_dotenv()

class MQTTPublisher:
    def __init__(self, broker_address, port, topic):
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
        self.client.username_pw_set(os.getenv("MQTT_ID_TC001"), os.getenv("MQTT_PASSWORD_TC001"))
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.connect(self.broker_address, self.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_publish(self, client, userdata, mid):
        print(f"Message published with mid: {mid}")

    def publish(self, message, endPrefix=""):
        full_topic = f"{self.topic}{endPrefix}"
        message_json = json.dumps(message)
        result = self.client.publish(full_topic, message_json)
        print(f"Publishing message to topic: {full_topic}")
        print(f"Message published: {message_json}")
        print(f"Publish result: {result.rc}, Message ID: {result.mid}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from broker")

class ClockMQTTPublisher(MQTTPublisher):
    def __init__(self):
        broker_address = os.getenv("MQTT_BROKER_ADDRESS")
        port = int(os.getenv("MQTT_PORT"))
        topic = os.getenv("MQTT_CLOCK_PREFIX")
        print(broker_address, port, topic)
        super().__init__(broker_address, port, topic)

    def publishJourneyDurationAndTrainStatus(self, message):
        endPrefix = "/custom/journeyDuration"
        super().publish(message, endPrefix)