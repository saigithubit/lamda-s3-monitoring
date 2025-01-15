import boto3
import csv
import time
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    try:
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        source_key = event['Records'][0]['s3']['object']['key']
        target_bucket = os.environ['TARGET_BUCKET']

        logger.info(f"Processing file: {source_key} from bucket: {source_bucket}")
        download_path = f"/tmp/{source_key.split('/')[-1]}"
        s3_client.download_file(source_bucket, source_key, download_path)

        start_time = time.time()
        transformed_data = transform_csv(download_path)
        processing_time = time.time() - start_time

        upload_key = f"processed/{source_key.split('/')[-1]}"
        upload_path = f"/tmp/transformed_{source_key.split('/')[-1]}"
        with open(upload_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(transformed_data)

        s3_client.upload_file(upload_path, target_bucket, upload_key)

        cloudwatch.put_metric_data(
            Namespace='LambdaMetrics',
            MetricData=[
                {'MetricName': 'RowsProcessed', 'Value': len(transformed_data) - 1, 'Unit': 'Count'},
                {'MetricName': 'ProcessingTime', 'Value': processing_time, 'Unit': 'Seconds'}
            ]
        )

        return {"statusCode": 200, "body": f"Processed {len(transformed_data) - 1} rows in {processing_time:.2f} seconds."}

    except Exception as e:
        logger.error(f"Error processing file: {e}")
        raise e

def transform_csv(file_path):
    transformed_data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        transformed_data.append(header + ["Transformed_Column"])
        for row in reader:
            transformed_data.append(row + [f"Transformed_{row[0]}"])
    logger.info(f"Transformed {len(transformed_data) - 1} rows.")
    return transformed_data