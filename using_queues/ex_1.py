import concurrent.futures
import functools
import logging
import logging.handlers
import multiprocessing
import os
from pprint import pprint
import threading
import time

from joblib import Parallel, delayed


def print_process_info():
    pid = os.getpid()
    pname = multiprocessing.current_process().name
    tid = threading.get_ident()
    tname = threading.current_thread().name
    print(f"in {pname} {pid}, {tid} {tname}")


def print_loggers_and_handlers():
    loggers = [logging.getLogger()]
    loggers.extend(
        filter(
            lambda l: not isinstance(l, logging.PlaceHolder),
            logging.root.manager.loggerDict.values(),
        )
    )
    pprint({l: l.handlers for l in loggers})


def set_up_logging(queue):
    queue_handler = logging.handlers.QueueHandler(queue)
    logging.root.addHandler(queue_handler)
    logging.root.setLevel("DEBUG")


def do_stuff(queue, set_up_logging_func):
    set_up_logging(queue)
    logger = logging.getLogger("my-app")
    print_loggers_and_handlers()
    logger.debug("debug")
    logger.info("info")
    logger.critical("critical")


class QueueListener(logging.handlers.QueueListener):
    def handle(self, record):
        print("QueueListener.handle called with", record)
        if record.name == "root":
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(record.name)
        if logger.isEnabledFor(record.levelno):
            # don't loggers already check record level?
            logger.handle(record)


if __name__ == "__main__":
    print_process_info()

    stream_handler = logging.StreamHandler()
    LOG_FORMAT = "%(asctime)s | %(process)d (%(processName)s) | %(thread)d %(threadName)s | %(levelname)s %(name)s | %(message)s"
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logging_queue = multiprocessing.Manager().Queue(-1)
    listener = logging.handlers.QueueListener(logging_queue, stream_handler)
    listener.start()

    print()
    print("in main thread")
    do_stuff(logging_queue, set_up_logging)
    time.sleep(0.01)

    print()
    print("in ProcessPoolExecutor")
    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        futures = [
            executor.submit(do_stuff, logging_queue, set_up_logging)
            for _ in range(2)
        ]
        print([f.result() for f in futures])
    time.sleep(0.1)

    print()
    print("in joblib.Parallel")
    log_some = functools.partial(do_stuff, logging_queue, set_up_logging)
    results = Parallel(n_jobs=2)(delayed(log_some)() for _ in range(2))
    print(results)
    time.sleep(0.1)

    listener.stop()
