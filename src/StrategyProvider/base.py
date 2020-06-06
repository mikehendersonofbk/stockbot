from abc import ABC, abstractmethod
from multiprocessing import Process, Queue

class StrategyProvider(ABC):
    def __init__(self):
        self.ingest_queue = Queue()
        self.analyze_queue = Queue()
        self.interest_queue = Queue()

    """ Abstract Method 'ingest_data'
        Receives new data and stores to internal
        Data structure if necessary
    """
    @abstractmethod
    def ingest_data(self, data):
        pass

    """ Abstract Method 'analyze'
        Used for analyzing dataset for a symbol
        To decide if interested in buying/selling
    """
    @abstractmethod
    def analyze(self):
        pass

    """ Abstract Method 'broadcast'
        Used for broadcasting interest in a postion
        on the broadcast_queue
    """
    @abstractmethod
    def broadcast(self, val):
        pass

    def run(self):
        ip = Process(target=self._ingest_worker)
        ip.start()
        ap = Process(target=self._analyze_worker)
        ap.start()

    def _ingest_worker(self):
        while True:
            data = self.ingest_queue.get()
            if data == 'DONE':
                return
            self.ingest_data(data)

    def _analyze_worker(self):
        while True:
            sym = self.analyze_queue.get()
            if sym == 'DONE':
                return
            self.analyze(sym)
