import boto3
import os 
from dotenv import load_dotenv
import json
import pandas as pd
import io

load_dotenv()

aws_access_key_id = os.environ['ACCESS_KEY_ID']
aws_secret_access_key = os.environ['SECRET_ACCESS_KEY']
aws_bucket = os.getenv('AWS_BUCKET')
cleaned_data = os.getenv('CLEANED_DATA')
raw_data = os.getenv('RAW_DATA')

s3 = boto3.client(
        's3',
        region_name = 'us-east-1',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key
    )

cleaned_data = s3.get_object(Bucket=aws_bucket,Key=cleaned_data)['Body'].read()
df = pd.read_excel(io.BytesIO(cleaned_data))
print(df)
