import subprocess
import logging

LOGGER = logging.getLogger(__name__) # this logger is defined seperately, see logging.conf

if __name__ == "__main__":
    
    # run celery worker as a subprocess
    LOGGER.info('starting subprocess celery worker')

    subprocess.Popen(
                        [
                            "celery",
                            "-A",
                            "celery_template",
                            "worker",
                            "-Q",
                            "celery_template_queue",
                            "--loglevel=DEBUG"
                        ]
                    )
