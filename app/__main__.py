import subprocess
import logging

from celery_template import logger

LOGGER = logging.getLogger(__name__) # this logger is defined seperately, see logging.conf

if __name__ == "__main__":
    
    LOGGER.info('starting celery_template app')
    
    # run celery worker as a subprocess
    subprocess.Popen(
                        [
                            "celery",
                            "-A",
                            "celery_template",
                            "worker",
                            "--loglevel=DEBUG"
                        ]
                    )
