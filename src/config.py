import os
from os.path import join, dirname
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv(join(dirname(__file__), '.env'))
        self.alpaca_data_addr = os.getenv('ALPACA_DATA_ADDRESS', 'https://data.alpaca.markets')
        self.alpaca_key_id = os.getenv('ALPACA_KEY_ID', None)
        self.alpaca_secret = os.getenv('ALPACA_SECRET', None)
        self.instruments = os.getenv('INSTRUMENT_LIST', 'AAPL,NFLX').split(',')
        self.quote_source = os.getenv('QUOTE_SOURCE', 'BackTest')