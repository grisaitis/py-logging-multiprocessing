import concurrent.futures
import logging
import os

logger = logging.getLogger("demo🙂")
logger.setLevel("DEBUG")

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        "%(process)d (%(processName)s) %(levelname)s:%(name)s:%(message)s"
    )
)
logger.addHandler(handler)


def get_logger_info(_=None):
    print(logger)
    another_logger = logging.getLogger("demo🙂")
    print(another_logger)
    # print(os.getpid(), "another_logger:", another_logger, another_logger.handlers)
    another_logger.warning(f"hello from {os.getpid()}")
    return another_logger


if __name__ == "__main__":
    print(get_logger_info())

    print()
    print("concurrent.futures demo...")
    with concurrent.futures.ProcessPoolExecutor(2) as executor:
        results = executor.map(get_logger_info, range(2))
        print(list(results))

    print()
    print("joblib demo (@amueller's example #2)...")
    from joblib import Parallel, delayed

    results = Parallel(n_jobs=2)(delayed(get_logger_info)() for _ in range(2))
    print(results)
