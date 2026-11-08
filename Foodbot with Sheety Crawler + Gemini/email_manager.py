import os
import smtplib
from email.message import EmailMessage
# from dotenv import load_dotenv

# load_dotenv()

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

class EmailManager:
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 465  # Port 465 requires SMTP_SSL

    def __init__(self):
        # Credentials loaded once as internal configuration constants
        self._sender_email = EMAIL
        self._app_password = PASSWORD
        if not self._sender_email or not self._app_password:
            raise ValueError("Email credentials ('sender_email' or 'app_password') not found in environment.")

    def send_email(self, recipients: list[str], subject: str, html_body: str) -> None:
        """Sends an HTML email using the pre-configured manager instance."""
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self._sender_email
        msg["To"] = ", ".join(recipients)  # Handles multiple recipients cleanly
        msg.set_content(html_body, subtype="html")

        try:
            with smtplib.SMTP_SSL(self.SMTP_HOST, self.SMTP_PORT) as server:
                server.login(self._sender_email, self._app_password)
                server.send_message(msg)
            print("Email sent successfully with special characters!")
        except Exception as e:
            print(f"An error occurred while sending email: {e}")
            raise
