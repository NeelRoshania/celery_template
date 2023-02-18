import logging
import logging.config

logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': f'logs/app_{__name__}.log'})