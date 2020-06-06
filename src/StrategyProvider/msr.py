from .base import StrategyProvider
import math
from datetime import datetime
from multiprocessing import Manager
import pytz

est = pytz.timezone('US/Eastern')
utc = pytz.utc
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

class MSRStrategyProvider(StrategyProvider):
    def __init__(self, settings):
        super().__init__()
        self.mgr = Manager()
        print('initializing MSR strategy')
        self.data = self.mgr.dict()
        self.instruments = settings['INSTRUMENTS']
        for ins in self.instruments:
            self.data[ins] = {
                'open': self.mgr.list(),
                'close': self.mgr.list(),
                'high': self.mgr.list(),
                'low': self.mgr.list(),
                'vol': self.mgr.list(),
                'time': self.mgr.list(),
            }
    
    def ingest_data(self, data):
        if data['symbol'] not in self.data.keys():
            return
        sym = data['symbol']
        self.data[sym]['open'].append(data['o'])
        self.data[sym]['close'].append(data['c'])
        self.data[sym]['high'].append(data['h'])
        self.data[sym]['low'].append(data['l'])
        self.data[sym]['vol'].append(data['v'])
        self.data[sym]['time'].append(data['t'])
        self.analyze_queue.put(sym)

    def analyze(self, sym):
        print('analyzing {}'.format(sym))
        curr = len(self.data[sym]['open']) - 1
        if self.is_green(sym, curr):
            print('{}:: green candle at {}'.format(sym, datetime.fromtimestamp(self.data[sym]['time'][curr]).astimezone(est).strftime(fmt)))
        elif self.is_red(sym, curr):
            print('red candle')
        return

    def broadcast(self):
        return

    def get_ochl_for_last(self, sym):
        ind = len(self.data[sym]['close']) - 1
        return self.get_ochl_for_index(sym, ind)

    def get_ochl_for_index(self, sym, index):
        return {
            'open': self.data[sym]['open'][index],
            'close': self.data[sym]['close'][index],
            'high': self.data[sym]['high'][index],
            'low': self.data[sym]['low'][index],
        }

    def is_green(self, sym, index):
        return self.data[sym]['close'][index] > self.data[sym]['open'][index]
    
    def is_red(self, sym, index):
        return self.data[sym]['close'][index] < self.data[sym]['open'][index]

    def is_indecision(self, sym, index):
        bar = self.get_ochl_for_index(sym, index)
        if abs(bar['high'] - bar['low']) / 2 > abs(bar['close'] - bar['open']):
            return True
        return False

    