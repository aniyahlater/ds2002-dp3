import boto3
from botocore.exceptions import ClientError
import requests
import json

# Set up your SQS queue URL and boto3 client
url = "https://sqs.us-east-1.amazonaws.com/440848399208/ybf3jw"
sqs = boto3.client('sqs')


messages_dict = {}

def get_message():
    message_amount = 10
    # going to attempt to apend the variables to a tuple
    for values in range (message_amount):
        try:
            # Receive message from SQS queue. Each message has two MessageAttributes: order and word
            # You want to extract these two attributes to reassemble the message
            response = sqs.receive_message(
                QueueUrl=url,
                AttributeNames=[
                    'All'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ]
            )
            # Check if there is a message in the queue or not
            if "Messages" in response:
                # extract the two message attributes you want to use as variables
                # extract the handle for deletion later
                order = response['Messages'][0]['MessageAttributes']['order']['StringValue']
                word = response['Messages'][0]['MessageAttributes']['word']['StringValue']
                handle = response['Messages'][0]['ReceiptHandle']

                # Print the message attributes - this is what you want to work with to reassemble the message
               # print(f"Order: {order}")
                #print(f"Word: {word}")

                message = {order: word}

                messages_dict.update(message)

            # If there is no message in the queue, print a message and exit    
            else:
                print("No message in the queue")
                continue
        
        # Handle any errors that may occur connecting to SQS
        except ClientError as e:
            print(e.response['Error']['Message'])

    print(messages_dict)
    # sort the dic
    sorted_dict = dict(sorted(messages_dict.items()))
    print(sorted_dict)
    # fetch out the VALUES of the dict, once it's sorted (another for loop)
    for each in sorted_dict:
        final_message = sorted_dict[each]
        print(final_message, end = ' ')
# Trigger the function
if __name__ == "__main__":
    get_message()

# going to simply enable this after i check in with the professor
"""
def delete_message(handle):
    try:
        # Delete message from SQS queue
        sqs.delete_message(
            QueueUrl=url,
            ReceiptHandle=handle
        )
        print("Message deleted")
    except ClientError as e:
        print(e.response['Error']['Message'])
        """