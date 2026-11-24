import boto3
from botocore.config import Config
from pydantic.types import SecretStr


class S3Client:
    def __init__(
        self,
        s3_endpoint: str,
        s3_access_key_id: str,
        s3_access_key_secret: SecretStr,
        s3_project_region: str,
    ):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=s3_endpoint,
            region_name=s3_project_region,
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_access_key_secret.get_secret_value(),
            config=Config(s3={"addressing_style": "path"}),
        )

    def close(self):
        self.s3_client.close()
