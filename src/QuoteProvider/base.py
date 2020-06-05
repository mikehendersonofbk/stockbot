from abc import ABC, abstractmethod
from multiprocessing import Process, Queue

class QuoteProviderBase(ABC):
    def __init__(self):
        self.broadcast_queue = Queue()

    """ Abstract Method 'fetch'
        Used for ingesting data from quote source.
        After fetching, put new data on provided queue.
    """
    @abstractmethod
    def fetch(self, q):
        pass

    """ Abstract Method 'broadcast'
        Used for broadcasting new quote data
        back to main process. Should translate fetched data
        to format that the selected StrategyProvider understands
    """
    @abstractmethod
    def broadcast(self, val):
        pass

    """ Method _run
        Forks a new process that calls 'fetch'.
        Continuously pulls off of queue to broadcast new records
        Until 'DONE' is found
    """
    def _run(self):
        q = Queue()
        p = Process(target=self.fetch, args=(q,))
        p.start()
        while True:
            msg = q.get()
            if msg == 'DONE':
                break
            self.broadcast(msg)
        p.join()

    """ Method 'run'
        Forks a new process to run internal _run method
        And returns control to main process
    """
    def run(self):
        q = Queue()
        p = Process(target=self._run)
        p.start()

