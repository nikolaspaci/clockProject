#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.services.WeatherStatusServices import publish_weather

if __name__ == "__main__":
    publish_weather("Paris")
