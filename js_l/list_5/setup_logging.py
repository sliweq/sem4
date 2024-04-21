import logging
import sys

logger = logging.getLogger()
def setup_logging(log : str) -> None:
    
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s <%(threadName)s> %(message)s",
    )
    
    match log:
        case "INFO":
            logger.setLevel(logging.INFO)
        case "DEBUG":
            logger.setLevel(logging.DEBUG)
        case "WARNING":
            logger.setLevel(logging.WARNING)
        case "ERROR":
            logger.setLevel(logging.ERROR)
        case "CRITICAL":
            logger.setLevel(logging.CRITICAL)
        case _:
            logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.addFilter(StdoutFilter())
    stdout_handler.setLevel(logging.DEBUG)
    logger.addHandler(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.addFilter(StderrFilter())
    logger.addHandler(stderr_handler)
    
class StdoutFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.WARNING

class StderrFilter(logging.Filter):
    def filter(self, record):
        return record.levelno > logging.WARNING
    