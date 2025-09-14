from ..backApiCaller.MarketApi import MarketApi
from ..mqtt.MQTTPublisher import ClockMQTTPublisher

class MarketService:
    def __init__(self):
        self.stock_api = MarketApi()
        self.mqtt_publisher = ClockMQTTPublisher()
        self.tickers = ["^FCHI", "^GSPC", "^IXIC", "^N225"]

    def get_stock_market_data(self):
        stock_data = []
        for ticker in self.tickers:
            data = self.stock_api.get_stock_data(ticker)
            if data:
                stock_data.append(data)
        return stock_data

    def format_and_publish_stock_data(self):
        stock_data = self.get_stock_market_data()
        if not stock_data:
            return

        apps = []
        for data in stock_data:
            icon = "50591" # Default icon
            if data["percent_change"] > 0:
                icon = "10372" # Arrow up
            elif data["percent_change"] < 0:
                icon = "10373" # Arrow down

            text = f'{data["name"]}: {data["percent_change"]:.2f}%'
            app = {
                "icon": icon,
                "text": text,
                "repeat": 1,
                "pushIcon": 2
            }
            apps.append(app)

        self.mqtt_publisher.publishStockMarket(apps)
