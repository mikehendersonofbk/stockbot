from QuoteProvider.backtester import BTQuoteProvider
from config import Config
import os
from multiprocessing import Queue

def quote_source_class(qs):
    if qs == 'BackTest':
        return BTQuoteProvider

def init_config():
    return Config()

def init_quote_provider(qs_cls, settings):
    return qs_cls(settings)

if __name__ == '__main__':
    config = init_config()
    print('running in process {}'.format(os.getpid()))
    print('Initializing quote source: {}'.format(config.quote_source))
    quote_provider = init_quote_provider(quote_source_class(config.quote_source), {
        'DATA_URL': config.alpaca_data_addr,
        'KEY_ID': config.alpaca_key_id,
        'SECRET': config.alpaca_secret,
        'INSTRUMENTS': config.instruments,
        'LIMIT': 1000,
    })
    quote_provider.run()

    while True:
        quote_msg = quote_provider.broadcast_queue.get()
        if quote_msg == 'DONE':
            break
        print('Got message from quote queue: {}'.format(quote_msg))
