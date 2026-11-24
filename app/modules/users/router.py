from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.dependencies import S3ServiceDep, SessionDep, UserDep, get_current_user
from app.modules.users.schemas import MeOutput, ProfilePictureUploadOutput
from app.modules.users.service import save_profile_picture

users_router = APIRouter(tags=["Users"], dependencies=[Depends(get_current_user)])


@users_router.get("/me", response_model=MeOutput)
async def me(user: UserDep):
    return user


@users_router.post("/upload/profile_picture", response_model=ProfilePictureUploadOutput)
async def upload_profile_picture(
    user: UserDep,
    profile_picture: UploadFile,
    session: SessionDep,
    s3_service: S3ServiceDep,
):
    if profile_picture.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=400, detail="Invalid image type")
    return await save_profile_picture(
        user.id,
        profile_picture.file,
        profile_picture.content_type,
        session,
        s3_service,
    )
