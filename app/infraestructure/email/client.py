import resend
from pydantic import SecretStr


class EmailClient:
    def __init__(self, api_key: SecretStr):
        resend.api_key = api_key.get_secret_value()

    async def send(self, params: resend.Emails.SendParams):
        return await resend.Emails.send_async(params)
