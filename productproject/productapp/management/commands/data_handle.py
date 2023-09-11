from django.core.management.base import BaseCommand
from productapp.models import Orders,Product,Seller,Customer,User
import pandas as pd
from celery import Celery
import logging

logger = logging.getLogger('root')


class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        # celery_app = Celery('productproject')
        # celery_app.worker_main(['celery', 'worker', '--loglevel=info'])
        try:
            dataframe=pd.read_excel("Product_data.xlsx")
            for index,row in dataframe.iterrows():
                print(index,type(row['product_name']),type(row['amount']))
                try:
                    Product.objects.create(
                        name=row['product_name'],
                        amount=row['amount'],
                    )
                    
                except Exception as e:
                    print(f'Product creation error occured :',e)
                    logger.error(f'Product creation error occurred: {e}')
                
            logger.info("products imported successfully")
        except Exception as e:
            print(f'An error occurred during product import: {e}')
            logger.error(f'An error occurred during product import: {e}')