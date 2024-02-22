import boto3
import os 
from dotenv import load_dotenv
import json
import pandas as pd
import io
import streamlit as st

load_dotenv()

aws_access_key_id = os.environ['ACCESS_KEY_ID']
aws_secret_access_key = os.environ['SECRET_ACCESS_KEY']
aws_bucket = os.getenv('AWS_BUCKET')
cleaned_data = os.getenv('CLEANED_DATA')
raw_data = os.getenv('RAW_DATA')

def aws_connection():
    s3 = boto3.client(
        's3',
        region_name = 'us-east-1',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key
    )
    return s3

def read_survey_data(data_key):
    s3 = aws_connection()
    online_survey = s3.get_object(Bucket=aws_bucket,Key=data_key)['Body'].read()
    df = pd.read_excel(io.BytesIO(online_survey))
    return df

