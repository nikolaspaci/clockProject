#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.services.CryptoService import CryptoService

if __name__ == "__main__":
    service = CryptoService()
    service.format_and_publish_crypto_data()
