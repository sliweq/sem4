import logging
import sys

class InfoDebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno <= logging.INFO

class WarningErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno > logging.INFO

# Utwórz instancję loggera
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Utwórz obsługiwacze dla stdout (info, debug) i stderr (warning, error)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(InfoDebugFilter())
logger.addHandler(stdout_handler)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.addFilter(WarningErrorFilter())
logger.addHandler(stderr_handler)

# Przykładowe użycie
logger.debug("To jest komunikat debugowy")
logger.info("To jest komunikat informacyjny")
logger.warning("To jest komunikat ostrzeżenia")
logger.error("To jest komunikat błędu")
