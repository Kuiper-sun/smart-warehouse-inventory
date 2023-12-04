import json
import csv
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def read_csv_from_s3(bucket, key):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        return response['Body'].read().decode('utf-8')
    except Exception as e:
        print(f"Error reading CSV from S3. Bucket: {bucket}, Key: {key}, Error: {e}")
        raise

def write_json_to_s3(bucket, key, data):
    try:
        json_data = json.dumps(data)
        s3.put_object(Body=json_data, Bucket=bucket, Key=key)
    except Exception as e:
        print(f"Error writing JSON to S3. Bucket: {bucket}, Key: {key}, Error: {e}")
        raise

def lambda_handler(event, context):
    # Extract information from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Adjust the key to include the "input/" prefix
    input_prefix = "input/"
    if not key.startswith(input_prefix):
        print(f"Error: Key {key} does not start with the expected prefix {input_prefix}.")
        return

    # Read CSV data from S3
    try:
        csv_data = read_csv_from_s3(bucket, key)
    except Exception as e:
        print(f"Error reading CSV from S3: {e}")
        return

    # Convert CSV to JSON (Example assumes CSV has headers)
    csv_reader = csv.DictReader(csv_data.splitlines())
    json_data = list(csv_reader)

    # Write JSON to S3 with timestamped folder structure
    current_datetime = datetime.utcnow()
    output_key = f"uploads/output/{current_datetime.year}/{current_datetime.month}/{current_datetime.day}/{current_datetime.strftime('%Y-%m-%d-%H-%M-%S')}.json"
    
    try:
        write_json_to_s3(bucket, output_key, json_data)
        print("CSV to JSON conversion and S3 write successful.")
    except Exception as e:
        print(f"Error writing JSON to S3: {e}")
        return