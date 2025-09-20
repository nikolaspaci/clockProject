#!/usr/bin/env python3

from src.services.WeatherStatusServices import publish_weather

if __name__ == "__main__":
    publish_weather("Paris")