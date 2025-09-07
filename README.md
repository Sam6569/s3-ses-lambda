 Prerequisites
 
Before you start, make sure you have:

An AWS account.

The AWS CLI configured with appropriate permissions.

Python 3.12 or later installed on your local machine.

A verified email address or domain in SES to send emails from. You'll need to do this in the SES console before you can send any notifications.

🛠️ Setup

Follow these steps to deploy and configure the project in your AWS account.

1. Create the S3 Bucket and Lambda Function
   
First, you'll need to create your S3 bucket and the Lambda function.

S3 Bucket: Go to the S3 console and create a new bucket. Give it a unique name (e.g., my-image-notification-bucket).

Lambda Function: Go to the Lambda console and create a new function.

Choose Author from scratch.

Name the function (e.g., S3ImageNotificationFunction).

Select Python 3.12 as the runtime.

Choose an execution role with permissions to access S3 and SES. An easy way to do this is to create a new role with basic Lambda permissions, and then attach the AmazonS3ReadOnlyAccess and AmazonSESFullAccess policies.

2. Configure the Lambda Code

Next, you'll add the Python code to your Lambda function.

In the Lambda console, navigate to your newly created function.

In the Code tab, copy and paste the following Python code into the lambda_function.py file.

Remember to replace your-verified-ses-email@example.com with the email address you verified in SES.

Python

import os
import boto3
import json

# Initialize the SES client
ses_client = boto3.client('ses', region_name=os.environ['AWS_REGION'])

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))

    # Get the S3 bucket and object key from the event
    try:
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
    except (KeyError, IndexError) as e:
        print(f"Error extracting S3 details: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps('Error: Invalid S3 event structure.')
        }

    # Define the email parameters
    sender_email = 'your-verified-ses-email@example.com' # Replace with your SES verified email
    recipient_email = 'recipient-email@example.com' # Replace with the recipient's email
    subject = f"New file uploaded to S3: {object_key}"
    body_text = f"A new file has been uploaded to the S3 bucket '{bucket_name}'.\n\nFile Name: {object_key}"

    # Send the email using SES
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [recipient_email]
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body_text
                    }
                }
            }
        )
        print("Email sent! Message ID: " + response['MessageId'])
    except Exception as e:
        print(f"Error sending email: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending email notification.')
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Email notification sent successfully!')
    }

3. Connect S3 and Lambda
This is the final step where you set up the S3 event notification to trigger your Lambda function.

In the Lambda console, go to your function's Configuration tab.

On the left, select Triggers.

Click Add trigger.

Choose S3 from the list of sources.

Select the S3 bucket you created earlier.

Choose the All object create events event type.

Check the box to enable the trigger.

Click Add. This will automatically grant the necessary permissions for S3 to invoke your Lambda function.

 Usage
To test the workflow, simply upload a file to your S3 bucket.

Navigate to your S3 bucket in the S3 console.

Click Upload.

Select a file (e.g., my-image.png) from your computer and upload it.

Within a few seconds, the S3 event will trigger your Lambda function, and an email notification will be sent to the recipient's email address you specified in the Lambda code.

Check the CloudWatch Logs for your Lambda function to monitor the execution and see the output.
