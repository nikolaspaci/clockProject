import yfinance as yf
import datetime

class MarketApi:
    def get_stock_data(self, ticker):
        stock = yf.Ticker(ticker)
        info = stock.info

        market_state = info.get('marketState', 'CLOSED')

        if market_state == 'REGULAR':
            current_price = info.get('regularMarketPrice')
            previous_close = info.get('previousClose')

            if current_price is None or previous_close is None:
                return None

            change = current_price - previous_close
            percent_change = (change / previous_close) * 100
        else:
            hist = stock.history(period="5d")

            if len(hist) < 2:
                return None

            last_close = hist['Close'].iloc[-1]
            previous_close = hist['Close'].iloc[-2]
            current_price = last_close

            change = last_close - previous_close
            percent_change = (change / previous_close) * 100

        return {
            "ticker": ticker,
            "name": info.get('longName', ticker),
            "current_price": current_price,
            "percent_change": percent_change
        }
