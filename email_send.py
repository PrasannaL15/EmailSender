import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Email credentials


SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))  # Ensure it's an integer
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Read recipient details from CSV file
csv_filename = "recipients.csv"
df = pd.read_csv(csv_filename)

# Read HTML email body
with open("email_body.html", "r", encoding="utf-8") as file:
    email_body = file.read()

# Attach Resume
resume_filename = "Resume.pdf"

# Function to send email
def send_email(to_email, name, role, company):
    try:
        # Set up the MIME message
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = f"Inquiry About {role} role"

        # Personalize email body
        personalized_body = email_body.replace("{name}", name)
        personalized_body = personalized_body.replace("{role}", role)
        personalized_body = personalized_body.replace("{copmany}", company)

        # Attach HTML body
        msg.attach(MIMEText(personalized_body, "html"))

        # Attach resume
        with open(resume_filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={resume_filename}")
            msg.attach(part)

        # Connect to SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()

        print(f"Email sent to {name} ({to_email}) successfully.")
    
    except Exception as e:
        print(f"Failed to send email to {name} ({to_email}): {e}")

# Send emails one by one
for index, row in df.iterrows():
    send_email(row["EmailID"], row["Name"], row['Role'], row['Company'])
