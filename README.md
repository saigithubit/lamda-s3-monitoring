Deployment Steps

Prepare Environment:

Install AWS CLI and Terraform.

Configure AWS CLI:

aws configure

Zip the Lambda code:

zip lambda_function.zip lambda_function.py

Deploy Infrastructure:

Initialize Terraform:

terraform init

Apply Configuration:

terraform apply -auto-approve

Validate Resources:

Verify S3 buckets, Lambda, and alarms in the AWS Management Console.

Testing

Test 1: Lambda Trigger

Upload a valid file to the source bucket:

aws s3 cp test_data.csv s3://<source_bucket>/

Verify processed files in the target bucket:

aws s3 ls s3://<target_bucket>/processed/

Test 2: Custom Metrics

Open the CloudWatch Metrics Console.

Check metrics under Custom Namespaces > LambdaMetrics:

RowsProcessed

ProcessingTime

Test 3: Alarms and Notifications

Trigger an error:

aws s3 cp malformed_data.csv s3://<source_bucket>/

Verify:

Error Alarm is triggered.

Email/Slack notification received.

Trigger high invocations:

for i in {1..10}; do aws s3 cp test_data.csv s3://<source_bucket>/test_data_$i.csv; done

Verify:

Invocation Alarm is triggered.

Notifications received.
