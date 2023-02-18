import argparse
import logging

from celery_template.tasks import add
from kombu.exceptions import OperationalError

"""

    Celery task execution
        - single tasks
        - grouped tasks

        - timed executions

"""
LOGGER = logging.getLogger(__name__) # will call the __main__ logger

if __name__ == "__main__":

    # LOGGER.info('testing scripted implementation')

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?")
    parser.add_argument("--optional", "-o", action="store", type=str, default=8000)
    args = parser.parse_args()

    # catch operational errors - perhaps cannot send message to worker
    try:
        res = add.apply_async(args=(5, 7), queue='celery_template')
        LOGGER.info(f'res: {res}, dir: {dir(res)}')
    except OperationalError as e: 
        LOGGER.debug(f'failed to execute tasks - {e}')

    