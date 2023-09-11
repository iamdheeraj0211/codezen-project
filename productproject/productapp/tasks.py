from celery import shared_task
from datetime import datetime
from django.core.management import call_command
import celery
import logging
logger=logging.getLogger('root')
@shared_task
def run_my_command():
    logger.info("celery mode")
    try:
        print("called celery mode")
        call_command("data_handle")
        logger.info("task completed successfully")
    except Exception as e:
        print("exception occured",e)
        logger.info("exception occured in celery mode",e)

        

# run_my_command()