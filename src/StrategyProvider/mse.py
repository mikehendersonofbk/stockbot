from .base import StrategyProvider

class MSEStrategyProvider(StrategyProvider):
    def __init__(self):
        super().__init__()
        print('initializing MSE strategy')
        self.data = {}
    
    def ingest_data(self, data):
        if data['symbol'] not in self.data.keys():
            self.data[data['symbol']] = {
                'open': [],
                'close': [],
                'high': [],
                'low': [],
                'vol': [],
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
        return

    def broadcast(self):
        return