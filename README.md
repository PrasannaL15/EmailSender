# Email Automation Utility

This utility automates sending personalized emails with attachments using Python. It reads recipient details from a CSV file, personalizes the email body using an HTML template, and sends the email with an attached PDF resume. Additionally, it allows users to preview the email before sending.

## Features

- Reads recipient details from a CSV file.
- Uses an HTML template for email body personalization.
- Attaches a PDF resume to each email.
- Sends emails securely using an SMTP server with `.env` configuration.
- **Email Preview**: Users can review the email content before sending.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required libraries from `requirements.txt`

## Installation

1. Clone this repository or download the files.
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Files Description

- `email_send.py`: The main script that sends personalized emails and provides a preview.
- `email_body.html`: The HTML template used for the email body.
- `recipients.csv`: The CSV file containing recipient details.
- `Resume.pdf`: The PDF resume attached to each email.
- `.env` (to be created): Stores SMTP credentials securely.
- `requirements.txt`: Lists required Python dependencies.

## CSV Format

The `recipients.csv` should have the following columns:

| Name     | EmailID             | Role              | Company | RoleAlignmentText            |
| -------- | ------------------- | ----------------- | ------- | ---------------------------- |
| John Doe | johndoe@example.com | Software Engineer | Google  | "Custom Role Alignment HTML" |

## Configuring SMTP Credentials

1. Create a `.env` file in the same directory as `email_send.py` and add:

   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   ```

   **Important:** If using Gmail, generate an **App Password** instead of using your actual password.

2. Ensure the `.env` file is added to `.gitignore` to prevent accidental sharing.

## Running the Script

Run the following command:

```bash
python email_send.py
```

This will send emails to all recipients listed in `recipients.csv` after allowing users to preview the email content.

## Notes

- If using Gmail, generate an **App Password** instead of using your actual password.

## Troubleshooting

- **Authentication Error**: Ensure correct email credentials and enable SMTP access.
- **CSV Issues**: Ensure the format matches the required structure.
- **Attachment Issues**: Confirm the file path and filename.

## License

This project is for personal use. Modify and distribute as needed.
