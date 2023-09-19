import argparse
import subprocess
import logging

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    # parser.add_argument("config", type=str, action="store", default="conf/config.yaml", nargs="?") # required
    parser.add_argument("--concurrency", "-c", default=1) # optional
    args = parser.parse_args()

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
                            f'--concurrency={args.concurrency}',
                            # "--logfile=logs/celery.log"
                        ]
                    )
    
    # # starting a flower instance
    # celery -A celery_template flower --port=5566 --loglevel=INFO
