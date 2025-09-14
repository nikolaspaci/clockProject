from ..mqtt.MQTTPublisher import ClockMQTTPublisher

class PowerService:
    def __init__(self):
        self.mqtt_publisher = ClockMQTTPublisher()

    def sleep(self, duration_in_seconds):
        payload = {"sleep": duration_in_seconds}
        self.mqtt_publisher.publishSleep(payload)
