import concurrent.futures
import logging
import os
from pprint import pprint

logger = logging.getLogger("william")
logger.setLevel("DEBUG")
logger.addHandler(logging.StreamHandler())


def get_logger_info(_=None):
    print(f"in process pid {os.getpid()}")
    l = logging.getLogger("william")
    return repr([l, l.handlers])


def main():
    print(f"from main process:")
    print(get_logger_info())

    print(f"from ProcessPoolExecutor:")
    with concurrent.futures.ProcessPoolExecutor(1) as executor:
        pprint(list(executor.map(get_logger_info, range(1))))


if __name__ == "__main__":
    # print()
    # print("updating logger")
    # logger = logging.getLogger("william")
    # logger.setLevel("INFO")

    # main()

    print()
    print("updating logger again")
    logger = logging.getLogger("william")
    logger.setLevel("DEBUG")
    logger.addHandler(logging.StreamHandler())

    print()
    main()
