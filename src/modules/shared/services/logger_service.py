import logging as logger

log_level = logger.DEBUG
log_format = '%(asctime)s - %(levelname)s - %(filename)s [%(lineno)d] (%(funcName)s): %(message)s'

logger.basicConfig(level=log_level, format=log_format)
