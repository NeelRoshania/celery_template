import argparse
import subprocess
import logging

LOGGER = logging.getLogger(__name__) # this logger is defined seperately, see logging.conf

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?") # need to define this
    parser.add_argument("--flower", "-f", const='', action="store_const")
    args = parser.parse_args()

    # run celery worker as a subprocess    
    if args.flower:
        LOGGER.info(f'starting celery worker node with flower - app:celery_template, queue: celery_template_queue, worker:worker')
        subprocess.Popen(
                            [
                                "celery",
                                "-A",
                                "celery_template",
                                "worker",
                                "-Q",
                                "celery_template_queue",
                                "--loglevel=INFO",
                                "flower",
                                "--port=5566"
                                # "--logfile=logs/celery.log"
                            ]
                        )
    else:
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
