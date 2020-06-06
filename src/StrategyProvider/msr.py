from .base import StrategyProvider
import math
from multiprocessing import Manager

class MSRStrategyProvider(StrategyProvider):
    def __init__(self):
        super().__init__()
        self.mgr = Manager()
        print('initializing MSR strategy')
        self.data = self.mgr.dict()
    
    def ingest_data(self, data):
        if data['symbol'] not in self.data.keys():
            self.data[data['symbol']] = {
                'open': self.mgr.list(),
                'close': self.mgr.list(),
                'high': self.mgr.list(),
                'low': self.mgr.list(),
                'vol': self.mgr.list(),
            }
        sym = data['symbol']
        self.data[sym]['open'].append(data['o'])
        self.data[sym]['close'].append(data['c'])
        self.data[sym]['high'].append(data['h'])
        self.data[sym]['low'].append(data['l'])
        self.data[sym]['vol'].append(data['v'])
        print('data: {}'.format(self.data))
        self.analyze_queue.put(sym)

    def analyze(self, sym):
        print('analyzing {}'.format(sym))
        curr = len(self.data[sym]['open']) - 1
        if self.is_green(sym, curr):
            print('green candle')
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

    