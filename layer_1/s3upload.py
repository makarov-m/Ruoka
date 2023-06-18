import boto3
import csv
from io import StringIO
import os
from dotenv import load_dotenv

# aws tokens
load_dotenv()
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
if not aws_access_key_id or not aws_secret_access_key:
    exit("Error: no token provided for aws")

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
s3 = session.resource('s3')

def write_csv_to_s3(bucket_name, file_name, data):
    # Create a string buffer to hold the CSV data
    csv_buffer = StringIO()

    # Write the data to the string buffer as CSV
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(data)

    # Upload the CSV file to S3
    s3.Object(bucket_name, file_name).put(Body=csv_buffer.getvalue())

bucket_name = 'ruokabot'
file_name = 'Wolkoff.csv'
data = [['Name', 'Age', 'Country'],
        ['John', 25, 'USA'],
        ['Emily', 30, 'UK']]

write_csv_to_s3(bucket_name, file_name, data)
