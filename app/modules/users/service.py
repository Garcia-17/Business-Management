from typing import BinaryIO
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.infraestructure.files.service import S3Service
from app.modules.users.repositories import update_profile_picture


async def save_profile_picture(
    user_id: UUID,
    profile_picture: BinaryIO,
    content_type: str,
    session: AsyncSession,
    s3_service: S3Service,
):
    profile_picture_id = uuid4()
    object_name = (
        f"{user_id}/profile_picture/{profile_picture_id}.{content_type.split('/')[1]}"
    )
    await s3_service.upload_file(
        "profile-pictures",
        object_name,
        profile_picture,
        content_type,
    )
    await update_profile_picture(user_id, object_name, session)
    return {
        "profile_picture_url": s3_service.get_file_url("profile-pictures", object_name)
    }
