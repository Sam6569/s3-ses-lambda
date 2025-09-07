# 📩 S3 → Lambda → SES Notification

This project demonstrates an AWS serverless workflow where an **image uploaded to Amazon S3** automatically triggers an **AWS Lambda function**, which then sends an **email notification via Amazon SES (Simple Email Service)**.

---

## 🚀 Workflow
1. A user uploads a `.png` (or any file) to the **S3 bucket**.
2. **S3 Event Notification** triggers the **Lambda function**.
3. The **Lambda function**:
   - Extracts the bucket and file name.
   - Sends an email notification using **SES**.
4. The recipient receives an email with the uploaded file details.

---

## 🛠️ Tech Stack
- **AWS S3** – File storage and event trigger.
- **AWS Lambda (Python 3.12)** – Serverless compute for processing the event.
- **Amazon SES** – Email notifications.
- **CloudWatch Logs** – Debugging and monitoring.

---

## 📂 Project Structure
