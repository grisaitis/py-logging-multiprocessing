import logging
import os
import sys

from joblib import Parallel, delayed

logger = logging.getLogger("sklearn")
logger.setLevel("DEBUG")

handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

print(os.getpid(), logger, logger.handlers)


def log_some():
    print(os.getpid(), logger, logger.handlers)
    another_logger = logging.getLogger("sklearn")
    print(os.getpid(), another_logger, another_logger.handlers)
    print(os.getpid(), logging.getLogger(), logging.getLogger().handlers)
    another_logger.critical("hello from joblib process")


results = Parallel(n_jobs=2)(delayed(log_some)() for _ in range(2))
