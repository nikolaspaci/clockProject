#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.services.PowerService import PowerService

if __name__ == "__main__":
    service = PowerService()
    service.sleep(25200)
