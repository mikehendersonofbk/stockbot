from QuoteProvider.backtester import BTQuoteProvider
from StrategyProvider.msr import MSRStrategyProvider
from config import Config
import os
from multiprocessing import Queue

def quote_source_class(qs):
    if qs == 'BackTest':
        return BTQuoteProvider

def strategy_class(ss):
    if ss == 'MSR':
        return MSRStrategyProvider

def init_config():
    return Config()

def init_quote_provider(qs_cls, settings):
    qp = qs_cls(settings)
    qp.run()
    return qp

def init_strategy_provider(ss_cls, settings):
    sp = ss_cls(settings)
    sp.run()
    return sp

def get_quotes(qp):
    while True:
        quote_msg = qp.broadcast_queue.get()
        if quote_msg == 'DONE':
            return
        yield quote_msg


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
    strategy_provider = init_strategy_provider(strategy_class(config.strategy_source), {
        'INSTRUMENTS': config.instruments,
    })

    for quote_msg in get_quotes(quote_provider):
        # print('Got message from quote queue: {}'.format(quote_msg))
        # print('submitting to strategy')
        strategy_provider.ingest_queue.put(quote_msg)