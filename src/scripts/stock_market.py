#!/usr/bin/env python3

from src.services.MarketService import MarketService

if __name__ == "__main__":
    service = MarketService()
    service.format_and_publish_stock_data()