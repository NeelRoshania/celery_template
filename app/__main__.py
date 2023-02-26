import argparse
import subprocess
import logging
import logging.config

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?") # need to define this
    parser.add_argument("--flower", "-f", const=True, action="store_const")
    args = parser.parse_args()

    # logging config
    logging.config.fileConfig(
        'conf/logging.conf', 
        defaults={
            'fileHandlerLog': f'logs/{__name__}.log'
            }
    )

    LOGGER = logging.getLogger(__name__) # this logger is defined seperately, see logging.conf

    # run celery worker as a subprocess
    LOGGER.info(f'starting celery worker node - app:celery_template, queue: celery_template_queue, worker:worker')
    subprocess.Popen(
                        [
                            "celery",
                            "-A",
                            "celery_template",
                            "worker",
                            "-Q",
                            "celery_template_queue",
                            "--loglevel=INFO",
                            # "--logfile=logs/celery.log"
                        ]
                    )
