from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.config import settings
from app.schemas import Token
from app.services import AuthService
from app.utils.exceptions import handle_exceptions
from app.db import DatabaseDep

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
@handle_exceptions
async def login(response: Response, db: DatabaseDep, form_data: OAuth2PasswordRequestForm = Depends()):
    tokens = await AuthService.login(form_data.username, form_data.password, db)

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
@handle_exceptions
async def refresh_token(request: Request, response: Response, db: DatabaseDep):
    refresh_t = request.cookies.get("refresh_token")
    tokens = await AuthService.refresh(refresh_t, db)

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer"
    }

@router.post("/logout")
@handle_exceptions
async def logout(response: Response):
    response.delete_cookie(key="refresh_token")
    return {"message": "logged out"}
