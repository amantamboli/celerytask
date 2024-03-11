from celery import Celery, shared_task
from celery.utils.log import get_task_logger
import csv
import json
import pandas as pd

@shared_task(bind=True,name='testing')
def testing(self):
    for i in range(10):
        print(i)
    return "Done"


# Task 1 Read data from students.csv
@shared_task(bind=True, name='task1')
def ReadCSV1(self):
    try:
        with open('students.csv', 'r') as csv_file:
            df = pd.read_csv(csv_file, nrows=3)
            json_result = df.to_json(orient='records', indent=2)
        print(json_result)
        return json_result

    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    
# Task 2 Read data from customer.csv    
@shared_task(bind=True, name='task2')
def csvRead(self):
    try:
        with open('customer.csv', 'r') as csv_file:
            df = pd.read_csv(csv_file, nrows=3)
            json_result = df.to_json(orient='records', indent=2)
        print(json_result)
        return json_result
    except FileNotFoundError as e:
        print(f"File not found error: {e}")


