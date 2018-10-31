""" Stolen from
#https://github.com/alistair-broomhead/python-logging-proxy/blob/master/src/python_logging_proxy/handlers.py

"""

import logging


def llen(x):
    if isinstance(x, list):
        return len(x)
    return len(list(x))

class StackingHandler(logging.Handler):
    """
    Logging handler for SQLite.
    Based on Vinay Sajip's DBHandler class
    (http://www.red-dove.com/python_logging.html)
    This version sacrifices performance for thread-safety:
    Instead of using a persistent cursor, we open/close connections for each
    entry.
    AFAIK this is necessary in multi-threaded applications,
    because SQLite doesn't allow access to objects across threads.
    """

    def __init__(self):
        logging.Handler.__init__(self)
        self.records = []
        self.messages = []

    def emit(self, record):
        self.records.append(record)

        # Use default formatting:
        self.format(record)
        if record.exc_info:
            record.exc_text = logging._defaultFormatter\
                                     .formatException(record.exc_info)
        else:
            record.exc_text = ""

        self.messages.append(record.exc_text)

        print(f'{llen(filter(bool, self.messages))} non empty messages')
        print(f'{llen(self.records)} records')


from pprint import pprint as print

def demo_stacking():
    """ does some simple demo for a very simple stacking handler"""
    logger = logging.getLogger()
    handler = StackingHandler()
    logger.addHandler(handler)
    logger.error('toto')
    try:
        1/0
    except Exception as exc:
        logger.exception(exc)
    print(handler.records)
    print(handler.messages)


if __name__ == '__main__':
    print("Demo for simple stacking logger ")
    demo_stacking()
    input('Press enter to continue :)')
