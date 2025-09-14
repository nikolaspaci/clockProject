from ..backApiCaller.MarketApi import MarketApi
from ..mqtt.MQTTPublisher import ClockMQTTPublisher

class CryptoService:
    def __init__(self):
        self.market_api = MarketApi()
        self.mqtt_publisher = ClockMQTTPublisher()
        self.tickers = ["BTC-USD", "ETH-USD", "XRP-USD"]

    def get_crypto_data(self):
        crypto_data = []
        for ticker in self.tickers:
            data = self.market_api.get_stock_data(ticker)
            if data:
                crypto_data.append(data)
        return crypto_data

    def format_and_publish_crypto_data(self):
        crypto_data = self.get_crypto_data()
        if not crypto_data:
            return

        apps = []
        icon_map = {
            "BTC-USD": "857",
            "ETH-USD": "9013",
            "XRP-USD": "18064"
        }
        for data in crypto_data:
            icon = icon_map.get(data["ticker"], "18064")
            if data["ticker"] in ["BTC-USD", "ETH-USD"]:
                text = f'${data["current_price"]:.2f}'
                push_icon = 0
                repeat = 2
            else:
                text = f'{data["ticker"].split("-")[0]}: ${data["current_price"]:.2f}'
                push_icon = 2
                repeat = 1
            app = {
                "icon": icon,
                "text": text,
                "repeat": repeat,
                "pushIcon": push_icon
            }
            apps.append(app)

        self.mqtt_publisher.publishCrypto(apps)
