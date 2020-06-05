from abc import ABC, abstractmethod
from multiprocessing import Process, Queue

class QuoteProviderBase(ABC):
    @abstractmethod
    def fetch(self):
        pass

    @abstractmethod
    def broadcast(self, val):
        pass

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


    def run(self):
        q = Queue()
        p = Process(target=self._run)
        p.start()

