from abc import ABC, abstractmethod
from multiprocessing import Process, Queue

class QuoteProviderBase(ABC):
    def __init__(self):
        self.fetch_queue = Queue()
        self.broadcast_queue = Queue()

    """ Abstract Method 'fetch'
        Used for ingesting data from quote source.
        Must be implemented as an iterator function.
    """
    @abstractmethod
    def fetch(self):
        pass

    """ Abstract Method 'broadcast'
        Used for broadcasting new quote data
        back to main process. Should translate fetched data
        to format that the selected StrategyProvider understands
    """
    @abstractmethod
    def broadcast(self, val):
        pass

    """ Method 'run'
        Forks a new process to run internal _run method
        And returns control to main process
    """
    def run(self):
        fp = Process(target=self._fetch_worker)
        fp.start()
        bp = Process(target=self._broadcast_worker)
        bp.start()

    """ Method _fetch_worker
        Runs a loop on the fetch iterator and puts
        any new data on self.fetch_queue
    """
    def _fetch_worker(self):
        for data in self.fetch():
            if data == 'DONE':
                self.fetch_queue.put('DONE')
                return
            self.fetch_queue.put(data)

    """ Method _broadcast_worker
        Runs a loop pulling from self.fetch_queue
        Calls self.broadcast on new data until sentinal
        value 'DONE' is reached
    """
    def _broadcast_worker(self):
        while True:
            msg = self.fetch_queue.get()
            if msg == 'DONE':
                return
            self.broadcast(msg)
