import logging

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s <%(threadName)s> %(message)s",
    )