import logging
# from celery_template import logging

LOGGER = logging.getLogger(__name__) # this calls the celery_template.funcs logger

def specific_func(text:str) -> None:

    """
        Log the argument

    """
    LOGGER.debug(text)

    return None