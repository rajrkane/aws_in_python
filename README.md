# aws_in_python

This is a simple Python script where I got my feet wet using the Amazon Web Services SDK with [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html). I became familiar with the basics of interacting with EC2 instances, S3 buckets, and SQS queues.

## Directory structure

The entire script is handled by one `main.py` file at the root of this directory. A possible re-structuring could have separate EC2, S3, and SQS modules with one main wrapper.

## Usage

First, set up your own keypair with AWS and enter them in the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` fields at the top of the script file.

Then, from the root of this directory, run `python main.py`.

## Tasks

The script accomplishes the following tasks in the specified order, as instructed in the project description:

1. Loads AWS SDK with Boto3, using access information
2. Sends a request to create an EC2 instance, one to create an S3 bucket, and one to create an SQS queue in that order
3. Waits for 1 minute
4. Lists all EC2 instances, S3 buckets, and SQS queues under current account in the current region
5. Uploads an empty text file with name `CSE546test.txt` into the newly created bucket
6. Sends a message with name `test message` and body `This is a test message` into the newly created queue
7. Records how many messages are in the newly created queue
8. Pulls the newly sent message and records its information
9. Again, records how many messages are in the queue
10. Sends a request to delete all the resources created thus far
11. Again, lists all EC2 instances, S3 buckets, and SQS queues under current account in the current region (the resources may not have been deleted yet)

## Output

Below is an example output.

```
$ python main.py
Running main.py

Loading SDK
Loaded EC2 resource and client
Loaded S3 client
Loaded SQS client

------------------------------------------------------------

Creating instance i-031067072e583dcf3

------------------------------------------------------------

Creating S3 bucket cse546-rajkane-bucket-ex4njl at http://cse546-rajkane-bucket-ex4njl.s3.amazonaws.com/

------------------------------------------------------------

Creating FIFO SQS queue
Queue name: cse546-rajkane-queue.fifo
URL: https://us-east-2.queue.amazonaws.com/604512611165/cse546-rajkane-queue.fifo

------------------------------------------------------------

Waiting 1 minute for creation
.
.
.
.
.
.
.
.
.
.
.
.

------------------------------------------------------------

Listing EC2 instance information
Instance ID: i-0330144315bbe94d8
State: terminated
AMI: ami-05803413c51f242b7
Platform: None
Type: t2.micro
Public IPv4 address: None

Instance ID: i-07bf5f8297bfacc95
State: running
AMI: ami-05803413c51f242b7
Platform: None
Type: t2.micro
Public IPv4 address: 18.221.90.130

Instance ID: i-031067072e583dcf3
State: running
AMI: ami-05803413c51f242b7
Platform: None
Type: t2.micro
Public IPv4 address: 18.116.239.173

------------------------------------------------------------

Listing S3 bucket information
Bucket name: cse546-rajkane-bucket-6tmo9u

Bucket name: cse546-rajkane-bucket-b6fvms

Bucket name: cse546-rajkane-bucket-djsfdv

Bucket name: cse546-rajkane-bucket-ejhstg

Bucket name: cse546-rajkane-bucket-ex4njl

Bucket name: cse546-rajkane-bucket-mkh4cp

Bucket name: cse546-rajkane-bucket-msdys5

------------------------------------------------------------

Listing SQS queue information
Queue name: cse546-rajkane-queue.fifo
URL: https://us-east-2.queue.amazonaws.com/604512611165/cse546-rajkane-queue.fifo

------------------------------------------------------------

Uploading file CSE546test.txt to bucket cse546-rajkane-bucket-ex4njl

------------------------------------------------------------

Sending message to SQS queue
Message ID: 1fefd11a-7967-4cc2-8d44-e4de0f5ae732
Name: test message
Body: This is a test message
Queue URL: https://us-east-2.queue.amazonaws.com/604512611165/cse546-rajkane-queue.fifo

------------------------------------------------------------

Number of messages in queue cse546-rajkane-queue.fifo: 1

------------------------------------------------------------

Received message from SQS queue
Message ID: 1fefd11a-7967-4cc2-8d44-e4de0f5ae732
Name: test message
Body: This is a test message
Queue URL: https://us-east-2.queue.amazonaws.com/604512611165/cse546-rajkane-queue.fifo

------------------------------------------------------------

Number of messages in queue cse546-rajkane-queue.fifo: 1

------------------------------------------------------------

Terminating instance i-031067072e583dcf3

------------------------------------------------------------

Cleaning up objects from bucket cse546-rajkane-bucket-ex4njl
Deleted file CSE546test.txt
Deleting bucket cse546-rajkane-bucket-ex4njl

------------------------------------------------------------

Deleting queue cse546-rajkane-queue.fifo

------------------------------------------------------------

Listing EC2 instance information
Instance ID: i-0330144315bbe94d8
State: terminated
AMI: ami-05803413c51f242b7
Platform: None
Type: t2.micro
Public IPv4 address: None

Instance ID: i-07bf5f8297bfacc95
State: running
AMI: ami-05803413c51f242b7
Platform: None
Type: t2.micro
Public IPv4 address: 18.221.90.130

Instance ID: i-031067072e583dcf3
State: shutting-down
AMI: ami-05803413c51f242b7
Platform: None
Type: t2.micro
Public IPv4 address: 18.116.239.173

------------------------------------------------------------

Listing S3 bucket information
Bucket name: cse546-rajkane-bucket-6tmo9u

Bucket name: cse546-rajkane-bucket-b6fvms

Bucket name: cse546-rajkane-bucket-djsfdv

Bucket name: cse546-rajkane-bucket-ejhstg

Bucket name: cse546-rajkane-bucket-mkh4cp

Bucket name: cse546-rajkane-bucket-msdys5

------------------------------------------------------------

Listing SQS queue information
Queue name: cse546-rajkane-queue.fifo
URL: https://us-east-2.queue.amazonaws.com/604512611165/cse546-rajkane-queue.fifo

------------------------------------------------------------
```
