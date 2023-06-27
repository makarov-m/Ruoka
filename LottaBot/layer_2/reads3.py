import boto3
import pandas as pd
from io import StringIO

s3 = boto3.client('s3')
bucket_name = 'ruokabot'
object_key = 'Wolkoff.csv'
response = s3.get_object(Bucket=bucket_name, Key=object_key)
body = response['Body']
csv_string = body.read().decode('utf-8')
df = pd.read_csv(StringIO(csv_string))
print(df.head())