from uuid import UUID

from pydantic import BaseModel, EmailStr


class MeOutput(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    verified: bool
    email: EmailStr
    profile_picture: str | None
    # exp: float


class ProfilePictureUploadOutput(BaseModel):
    success: bool = True
    profile_picture_url: str
