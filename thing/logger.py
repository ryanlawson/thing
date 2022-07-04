import logging as logger, os

LOG_LEVELS = {
    'DEBUG': logger.DEBUG,
    'INFO': logger.INFO,
    'WARN': logger.WARN,
    'ERROR': logger.ERROR
}

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

logger.basicConfig(level=LOG_LEVELS[log_level])
