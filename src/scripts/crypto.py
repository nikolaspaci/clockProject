#!/usr/bin/env python3

from src.services.CryptoService import CryptoService

if __name__ == "__main__":
    service = CryptoService()
    service.format_and_publish_crypto_data()