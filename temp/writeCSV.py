#!/usr/bin/env python
import os
from datetime import datetime
import csv

def write_user_info(user_id, timestamp):
    file_exists = os.path.isfile('user_info.csv')
    with open('user_info.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if not file_exists:
            writer.writerow(['User ID', 'Timestamp'])  # Write header if the file is newly created
        writer.writerow([user_id, timestamp])

user_id = "makarovm"
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

write_user_info(user_id, timestamp)