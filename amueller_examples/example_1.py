import logging
from pprint import pprint

from joblib import Parallel, delayed

logger = logging.getLogger("sklearn")
logger.setLevel(2)
pprint(logging.Logger.manager.loggerDict)


def get_level():
    pprint(logging.Logger.manager.loggerDict)
    another_logger = logging.getLogger("sklearn")
    return another_logger.level


results = Parallel(n_jobs=2)(delayed(get_level)() for _ in range(2))

print(results)
