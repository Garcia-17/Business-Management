from fastapi import APIRouter

from app.modules.auth.router import auth_router
from app.modules.users.router import users_router

api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(users_router, prefix="/user")
