import resend
from pydantic import SecretStr

from app.infraestructure.email.client import EmailClient
from app.infraestructure.email.templates import render_template


class EmailService:
    def __init__(self, api_key: SecretStr, app_name: str):
        self.email_client = EmailClient(api_key)
        self.app_name = app_name

    async def send_verification_email(
        self, username: str, email: str, verification_token: str
    ):
        params: resend.Emails.SendParams = {
            "from": "onboarding@resend.dev",
            "to": [email],
            "subject": "Please verify your email",
            "html": render_template(
                "email_verification.html",
                {
                    "title": "Email verification request",
                    "app_name": self.app_name,
                    "username": username,
                    "verification_url": f"http://localhost:8000/api/v1/auth/verify?token={verification_token}",
                },
            ),
        }
        await self.email_client.send(params)
