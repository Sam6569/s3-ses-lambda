import json
import boto3
import urllib.parse

s3 = boto3.client("s3")
ses = boto3.client("ses")

# Replace with your verified sender & recipient emails in SES
SENDER = "your-verified-sender@example.com"
RECIPIENT = "your-verified-recipient@example.com"

def lambda_handler(event, context):
    print("Received event:", json.dumps(event, indent=2))

    try:
        # Extract bucket and object info from the event
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        
        # Build the email content
        subject = f"S3 Upload Notification: {key}"
        body = (
            f"A new file has been uploaded to your S3 bucket.\n\n"
            f"Bucket: {bucket}\n"
            f"Key: {key}\n"
        )

        # Send email via SES
        response = ses.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [RECIPIENT]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}}
            }
        )

        print("SES response:", response)
        return {"statusCode": 200, "body": "Email sent successfully!"}

    except Exception as e:
        print("Error:", str(e))
        return {"statusCode": 500, "body": str(e)}
