from celery import Celery, shared_task
from celery.utils.log import get_task_logger
import time
logger = get_task_logger(__name__)
from celery.result import AsyncResult
import csv
import json


@shared_task(bind=True,name='testing')
def testing(self):
    for i in range(10):
        print(i)
    return "Done"



@shared_task(bind=True, name='task1')
def ReadCSV1(self):


    try:
        with open('students.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data = [row for index, row in enumerate(csv_reader) if index < 3]

        # Convert the data to JSON format
        json_data = json.dumps(data, indent=2)

        return json_data
    except FileNotFoundError as e:
        # Log the error for debugging
        print(f"File not found error: {e}")
        
@shared_task(bind=True, name='task2')
def csvRead(self):

    try:
        # Read CSV file and convert to a list of dictionaries (limit to last 3 rows)
        with open('students.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Use a list to store the last 3 rows
            last_three_rows = []

            for row in csv_reader:
                last_three_rows.append(row)
                if len(last_three_rows) > 3:
                    last_three_rows.pop(0)  # Trim the list to keep only the last 3 rows

        # Convert the data to JSON format
        json_data = json.dumps(last_three_rows, indent=2)

        return json_data
    except FileNotFoundError as e:
        # Log the error for debugging
        print(f"File not found error: {e}")


