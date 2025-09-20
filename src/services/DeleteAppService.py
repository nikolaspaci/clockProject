from ..mqtt.MQTTPublisher import ClockMQTTPublisher

class DeleteAppService:
    def __init__(self):
        self.mqtt_publisher = ClockMQTTPublisher()

    def delete_app(self, app_name):
        """
        Deletes a custom app by publishing an empty message to its topic.
        """
        self.mqtt_publisher.publish({}, f"/custom/{app_name}")
        print(f"Sent delete request for app: {app_name}")

    def delete_transport_apps(self):
        """
        Deletes all custom apps related to transport.
        """
        self.delete_app("journeyDuration")

    def delete_financial_apps(self):
        """
        Deletes all custom apps related to financial values.
        """
        self.delete_app("stock")
        self.delete_app("crypto")

    def delete_all_apps(self):
        """
        Deletes all transport and financial custom apps.
        """
        self.delete_transport_apps()
        self.delete_financial_apps()
        self.mqtt_publisher.disconnect()

if __name__ == '__main__':
    # Example of how to use the service to delete all apps
    cleanup_service = DeleteAppService()
    cleanup_service.delete_all_apps()
