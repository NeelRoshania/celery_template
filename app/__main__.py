import subprocess

from celery_template import logger

if __name__ == "__main__":
    
    logger.info('starting celery_template app')
    
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
