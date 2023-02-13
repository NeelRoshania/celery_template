import logging
import logging.config

logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': 'logs/app.log'})