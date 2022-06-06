import time
import boto3
import string
import random

__author__ = "Raj Kane"
__email__ = "rajrkane@asu.edu"
__version__ = "05-06-2022"

# Enter access info here
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
REGION = 'us-east-2'
AMI_ID = 'ami-05803413c51f242b7'

def load_sdk():
	'''Loads EC2 resource and client, S3 client, and SQS client using Boto3.'''

	print('\nLoading SDK')
	(ec2_resource, ec2_client) = load_ec2()
	s3_client = load_s3()
	sqs_client = load_sqs()
	print('\n' + '-' * 60)

	return ec2_resource, ec2_client, s3_client, sqs_client

def load_ec2():
	'''Returns newly loaded EC2 resource and client.'''

	ec2_resource = boto3.resource(
		'ec2',
		region_name=REGION,
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY
	)
	ec2_client = boto3.client(
		'ec2',
		region_name=REGION,
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY
	)

	print('Loaded EC2 resource and client')

	return ec2_resource, ec2_client

def load_s3():
	'''Returns newly loaded S3 client.'''

	s3_client = boto3.client(
		's3',
		region_name=REGION,
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY
	)

	print('Loaded S3 client')

	return s3_client

def load_sqs():
	'''Returns newly loaded SQS client.'''
	sqs_client = boto3.client(
		'sqs',
		region_name=REGION,
		aws_access_key_id=AWS_ACCESS_KEY_ID,
		aws_secret_access_key=AWS_SECRET_ACCESS_KEY
	)

	print('Loaded SQS client')

	return sqs_client

def create_instance(ec2_resource):
	'''Creates an EC2 instance. Takes in an EC2 resource. Returns the instance ID.'''

	instance = ec2_resource.create_instances(
		ImageId=AMI_ID,
		MinCount=1,
		MaxCount=1,
		InstanceType='t2.micro',
		TagSpecifications=[{
			'ResourceType': 'instance',
			'Tags': [{
				'Key': 'Name',
				'Value': 'cse546-rajkane-instance'
			}]
		}]
	)

	inst_id = str(instance[0]).split("id='", 1)[1].split("')", 1)[0]
	print('\nCreating instance', inst_id)
	print('\n' + '-' * 60)

	return inst_id

# Terminate instance
def terminate_instance(ec2_client, inst_id):
	'''Terminates an EC2 instance. Takes in an EC2 client and the instance ID.'''

	response = ec2_client.terminate_instances(
		InstanceIds=[inst_id]
	)

	print('\nTerminating instance', inst_id)
	print('\n' + '-' * 60)

def list_instances(ec2_resource):
	'''Lists all EC2 instances in this account in the current region. Takes in an EC2 resource.'''

	print('\nListing EC2 instance information')
	instances = ec2_resource.instances.all()

	if instances:
		for inst in instances:
			print(f'Instance ID: {inst.id}')
			print(f'State: {inst.state["Name"]}')
			print(f'AMI: {inst.image.id}')
			print(f'Platform: {inst.platform}')
			print(f'Type: {inst.instance_type}')
			print(f'Public IPv4 address: {inst.public_ip_address}\n')
	else:
		print('No instances found')

	print('-'*60)

def create_bucket(s3_client):
	'''Creates an S3 bucket. Takes in an S3 client. Returns the bucket URL.'''

	# Create unique name, since bucket namespace is shared globally
	nonce = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))
	bucket_name = "cse546-rajkane-bucket-" + nonce

	response = s3_client.create_bucket(
		Bucket=bucket_name,
		CreateBucketConfiguration={
			"LocationConstraint": REGION
		}
	)

	bucket_url = response['Location']
	bucket_name = bucket_url.split('/')[-2].split('.')[0]

	print('\nCreating S3 bucket', bucket_name, 'at', bucket_url)
	print('\n' + '-' * 60)

	return bucket_url

def cleanup_bucket(s3_client, bucket_name):
	'''Deletes all objects from an S3 bucket. Called before bucket deletion. Takes in an S3 client and the bucket name.'''

	print('\nCleaning up objects from bucket', bucket_name)
	objects = s3_client.list_objects(Bucket=bucket_name)['Contents']
	for obj in objects:
		obj_name = obj['Key']
		s3_client.delete_object(Bucket=bucket_name, Key=obj_name)
		print('Deleted file', obj_name)

def delete_bucket(s3_client, bucket_url):
	'''Deletes an S3 bucket. Takes in an S3 client and the bucket URL.'''

	bucket_name = bucket_url.split('/')[-2].split('.')[0]
	cleanup_bucket(s3_client, bucket_name)

	s3_client.delete_bucket(Bucket=bucket_name)

	print('Deleting bucket', bucket_name)
	print('\n' + '-' * 60)

def list_buckets(s3_client):
	'''Lists all S3 buckets in this account in the current region. Takes in an S3 client.'''

	print('\nListing S3 bucket information')
	buckets = s3_client.list_buckets()

	if 'Buckets' in buckets:
		for buck in buckets['Buckets']:
			print(f"Bucket name: {buck['Name']}\n")
	else:
		print('No buckets found')

	print('-'*60)

def upload_file(s3_client, bucket_url, file_name, object_name=None):
	'''Creates an empty text file and uploads it into an S3 bucket. Takes in an S3 client, the bucket URL, the file name, and optionally the object name.'''

	# Create empty file
	open(file_name, 'a').close()

	if object_name is None:
		object_name = file_name

	bucket_name = bucket_url.split('/')[-2].split('.')[0]
	s3_client.upload_file(file_name, bucket_name, object_name)

	print(f'\nUploading file {file_name} to bucket {bucket_name}')
	print('\n' + '-' * 60)

def create_queue(sqs_client):
	'''Creates an SQS queue. Takes in an SQS client. Returns the queue URL.'''

	response = sqs_client.create_queue(
		QueueName="cse546-rajkane-queue.fifo",
		Attributes={
			"DelaySeconds": "0",
			"VisibilityTimeout": "60",
			"FifoQueue": "true",
		}
	)

	q_url = response['QueueUrl']
	q_name = q_url.split('/')[-1]

	print('\nCreating FIFO SQS queue')
	print('Queue name:', q_name)
	print('URL:', q_url)
	print('\n' + '-' * 60)

	return q_url

def delete_queue(sqs_client, q_url):
	'''Deletes an SQS queue. Takes in an SQS client and the queue URL.'''

	response = sqs_client.delete_queue(QueueUrl=q_url)
	q_name = q_url.split('/')[-1]
	print('\nDeleting queue', q_name)
	print('\n' + '-' * 60)

def list_queues(sqs_client):
	'''Lists all SQS queues in this account in the current region. Takes in an SQS client.'''

	print('\nListing SQS queue information')
	queues = sqs_client.list_queues()

	if 'QueueUrls' in queues:
		for q in queues['QueueUrls']:
			print(f'Queue name: {q.split("/")[-1]}')
			print(f'URL: {q}\n')
	else:
		print('No queues found')

	print('-'*60)

def send_message(sqs_client, q_url, msg_name, msg_body):
	'''Sends a message into an SQS queue. Takes in an SQS client, the queue URL, the message name attribute, and the message body. Returns the message ID.'''

	response = sqs_client.send_message(
		QueueUrl=q_url,
		MessageAttributes={
			'Name': {
				'DataType': 'String',
				'StringValue': msg_name			}
		},
		MessageBody=msg_body,
		MessageGroupId='1',
		MessageDeduplicationId=str(int(time.time())+1)
	)

	msg_id = response['MessageId']
	print('\nSending message to SQS queue')
	print('Message ID:', msg_id)
	print('Name:', msg_name)
	print('Body:', msg_body)
	print('Queue URL:', q_url)
	print('\n' + '-' * 60)

	return msg_id

def count_messages(sqs_client, q_url):
	'''Counts the approximate number of messages in a queue. Takes in an SQS client and the queue URL.'''

	response = sqs_client.get_queue_attributes(
		QueueUrl=q_url,
		AttributeNames=['ApproximateNumberOfMessages']
	)

	msg_count = response['Attributes']['ApproximateNumberOfMessages']
	q_name = q_url.split("/")[-1]
	print(f'\nNumber of messages in queue {q_name}: {msg_count}')
	print('\n' + '-' * 60)

def receive_message(sqs_client, q_url, msg_id):
	'''Pulls a given message from an SQS queue and lists its properties. Takes in an SQS client, the queue URL, and the message ID.'''

	response = sqs_client.receive_message(
		QueueUrl=q_url,
		MessageAttributeNames=['Name'],
		AttributeNames=['All'],
		MaxNumberOfMessages=10
	)

	msg = list(filter(lambda m: m['MessageId']==msg_id, response['Messages']))[0]
	msg_name = msg['MessageAttributes']['Name']['StringValue']
	msg_body = msg['Body']

	print('\nReceived message from SQS queue')
	print('Message ID:', msg_id)
	print('Name:', msg_name)
	print('Body:', msg_body)
	print('Queue URL:', q_url)
	print('\n' + '-' * 60)

def main():
	print('Running main.py')

	# Load SDK
	ec2_resource, ec2_client, s3_client, sqs_client = load_sdk()

	# Create resources
	inst_id = create_instance(ec2_resource)
	bucket_url = create_bucket(s3_client)
	q_url = create_queue(sqs_client)

	# Wait for AWS to create resources
	print('\nWaiting 1 minute for creation')
	for i in range(12):
		time.sleep(5)
		print('.')
	print('\n' + '-' * 60)

	# List resources
	list_instances(ec2_resource)
	list_buckets(s3_client)
	list_queues(sqs_client)

	# Upload file to S3
	file_name='CSE546test.txt'
	upload_file(s3_client, bucket_url, file_name)

	# Send message to SQS, get message count, pull the sent message, count again
	msg_name = 'test message'
	msg_body = 'This is a test message'
	msg_id = send_message(sqs_client, q_url, msg_name, msg_body)
	count_messages(sqs_client, q_url)
	receive_message(sqs_client, q_url, msg_id)
	count_messages(sqs_client, q_url)

	# Delete resources
	terminate_instance(ec2_client, inst_id)
	delete_bucket(s3_client, bucket_url)
	delete_queue(sqs_client, q_url)

	# List resources again
	list_instances(ec2_resource)
	list_buckets(s3_client)
	list_queues(sqs_client)

if __name__=="__main__":
	main()
