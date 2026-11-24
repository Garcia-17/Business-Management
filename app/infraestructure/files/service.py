import asyncio
from typing import BinaryIO

from pydantic.types import SecretStr

from app.infraestructure.files.client import S3Client


class S3Service:
    def __init__(
        self,
        s3_endpoint: str,
        s3_access_key_id: str,
        s3_access_key_secret: SecretStr,
        s3_project_region: str,
    ):
        self.s3_public_endpoint: str = s3_endpoint + "/object/public"
        self.s3_client = S3Client(
            s3_endpoint + "/s3",
            s3_access_key_id,
            s3_access_key_secret,
            s3_project_region,
        )

    async def upload_file(
        self, bucket: str, object_name: str, file: BinaryIO, content_type: str
    ):
        return await asyncio.to_thread(
            self.s3_client.s3_client.upload_fileobj,
            file,
            bucket,
            object_name,
            ExtraArgs={"ContentType": content_type or "application/octet-stream"},
        )

    def get_file_url(self, bucket: str, object_name: str):
        return f"{self.s3_public_endpoint}/{bucket}/{object_name}"

    def close(self):
        self.s3_client.close()
