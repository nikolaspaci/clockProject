from ..mqtt.MQTTPublisher import ClockMQTTPublisher

class PowerService:
    def __init__(self):
        self.mqtt_publisher = ClockMQTTPublisher()

    def sleep(self, duration_in_seconds):
        payload = {"sleep": duration_in_seconds}
        self.mqtt_publisher.publishSleep(payload)

    def turn_on(self):
        payload = {"power": True}
        self.mqtt_publisher.publishPower(payload)

    def turn_off(self):
        payload = {"power": False}
        self.mqtt_publisher.publishPower(payload)
