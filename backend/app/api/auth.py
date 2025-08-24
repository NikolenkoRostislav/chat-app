from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from app.config import settings
from app.db.session import get_db
from app.schemas import Token
from app.services import AuthService
from app.utils.exceptions import handle_exceptions

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
@handle_exceptions
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    tokens = await AuthService.login(form_data.username, form_data.password, db)

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
@handle_exceptions
async def refresh_token(refresh_token: str, response: Response, db: AsyncSession = Depends(get_db)):
    tokens = await AuthService.refresh(refresh_token, db)

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer"
    }
