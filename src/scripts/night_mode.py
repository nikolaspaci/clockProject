#!/usr/bin/env python3

from src.services.PowerService import PowerService

if __name__ == "__main__":
    service = PowerService()
    service.sleep(25200)