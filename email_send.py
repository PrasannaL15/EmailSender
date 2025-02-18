import pandas as pd
import os
import smtplib
import tkinter as tk
from tkinter import messagebox
from tkhtmlview import HTMLLabel  # Import HTML rendering widget
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

def process_email_body(name, role, company, RoleAlignmentText):
    return email_body.replace("{name}", name)\
                                  .replace("{role}", role)\
                                  .replace("{company}", company)\
                                  .replace("{RoleAlignmentText}", RoleAlignmentText)

# Function to show popup preview before sending email
def preview_email(to_email, name, role, company, RoleAlignmentText):
    preview_window = tk.Tk()
    preview_window.title("Email Preview")
    preview_window.attributes("-topmost", True)
    preview_window.geometry("1100x800")
    email_subject = f"Inquiry About {role} role"
    personalized_body = process_email_body(name, role, company, RoleAlignmentText)

    # Display To and Subject
    tk.Label(preview_window, text=f"To: {to_email}", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(preview_window, text=f"Subject: {email_subject}", font=("Arial", 10, "bold")).pack(pady=5)

    # Display Email Body with HTML Rendering
    html_label = HTMLLabel(preview_window, html=personalized_body, width=80, height=20)
    html_label.pack(pady=10, padx=10, fill="both", expand=True)

    # Function to proceed with sending email
    def send_email():
        preview_window.destroy()
        send_actual_email(to_email, name, role, company, RoleAlignmentText)

    # Buttons to Confirm or Cancel
    btn_frame = tk.Frame(preview_window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Send Email", command=send_email, fg="white", bg="green", width=15).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Cancel", command=preview_window.destroy, fg="white", bg="red", width=15).grid(row=0, column=1, padx=10)

    preview_window.mainloop()

# Function to send email
def send_actual_email(to_email, name, role, company, RoleAlignmentText):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = f"Inquiry About {role} role"

        personalized_body = process_email_body(name, role, company, RoleAlignmentText)

        msg.attach(MIMEText(personalized_body, "html"))

        with open(resume_filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={resume_filename}")
            msg.attach(part)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Success", f"Email sent to {name} ({to_email}) successfully.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email to {name} ({to_email}): {e}")

# Process each email one by one with preview
for index, row in df.iterrows():
    preview_email(row["EmailID"], row["Name"], row['Role'], row['Company'], row['RoleAlignmentText'])
