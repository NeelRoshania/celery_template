import logging
# from celery_template import logging

LOGGER = logging.getLogger(__name__) # this calls the celery_template.funcs logger
logging.config.fileConfig('conf/logging.conf', defaults={'fileHandlerLog': f'logs/{__name__}.log'}) # this will call celery_template.funcs

def specific_func(text:str) -> None:

    """
        Log the argument

    """
    LOGGER.debug(text)

    return None
