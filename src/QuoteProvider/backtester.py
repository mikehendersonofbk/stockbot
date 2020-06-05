from .base import QuoteProviderBase
import time
import requests
import os
from multiprocessing import Queue

class BTQuoteProvider(QuoteProviderBase):
    def __init__(self, settings):
        print('init backtest queue in process: {}'.format(os.getpid()))
        print('fetching data from alpaca for instruments {}'.format(','.join(settings['INSTRUMENTS'])))
        self.data_url = settings['DATA_URL']
        self.alpaca_key_id = settings['KEY_ID']
        self.alpaca_secret = settings['SECRET']
        self.instruments = settings['INSTRUMENTS']
        self.limit = settings['LIMIT']
        self._gather_historical_data()
        self.broadcast_queue = Queue()

    def _gather_historical_data(self):
        params = { 'symbols': ','.join(self.instruments), 'limit': self.limit }
        headers = {'APCA-API-KEY-ID': self.alpaca_key_id, 'APCA-API-SECRET-KEY': self.alpaca_secret }
        data = requests.get('{}/v1/bars/1Min'.format(self.data_url), params=params, headers=headers)
        self.data = data.json()

    def fetch(self, q):
        print('fetching in process: {}'.format(os.getpid()))
        for i in range(self.limit):
            time.sleep(1)
            for instrument in self.instruments:
                q.put(self.data[instrument][i])
        q.put('DONE')

    def broadcast(self, val):
        self.broadcast_queue.put(val)