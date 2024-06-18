import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_personalized_email(smtp_server, port, sender_email, sender_password, recipient_email, subject, body):
    # Create the message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the message via the SMTP server
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def main():
    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_password'
    
    # Email subject template
    subject_template = "Hello {name}, Here's Your Personalized Email!"
    
    # Path to the CSV file
    current_dir = os.path.dirname(__file__)
    print(f"Current directory: {current_dir}")
    
    csv_file_path = os.path.join(current_dir, 'recipients.csv')
    print(f"Looking for file at: {csv_file_path}")
    
    # List the contents of the current directory
    print("Directory contents:", os.listdir(current_dir))
    
    # Check if the file exists
    if not os.path.exists(csv_file_path):
        print(f"File not found: {csv_file_path}")
        return
    
    # Read the recipient list from CSV
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            recipient_email = row['Email']
            personalized_message = row['Message']  # Adjust according to your CSV columns
            
            # Email body template
            body = f"Dear {name},\n\n{personalized_message}\n\nBest regards,\nYour Company"
            
            # Send the email
            try:
                send_personalized_email(smtp_server, port, sender_email, sender_password, recipient_email, subject_template.format(name=name), body)
                print(f"Email sent to {name} ({recipient_email})")
            except Exception as e:
                print(f"Failed to send email to {name} ({recipient_email}): {str(e)}")
                
