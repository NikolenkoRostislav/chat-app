from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import ChatCreate, ChatRead, ChatMemberRead
from app.services import ChatService
from app.utils.auth import get_current_user
from app.utils.exceptions import handle_exceptions
from app.models import Chat, User

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatRead)
@handle_exceptions
async def create_chat(chat: ChatCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatService.create_chat(chat, db, current_user)

@router.get("/{chat_id}", response_model=ChatRead)
@handle_exceptions
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    return await ChatService.get_chat_by_id(chat_id, db, True) 

@router.get("/members/{chat_id}", response_model=list[ChatMemberRead])
@handle_exceptions
async def get_chat_members(chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatService.get_chat_members_by_chat_id(chat_id, db, current_user)

@router.get("/member-count/{chat_id}")
@handle_exceptions
async def get_chat_member_count(chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatService.get_chat_member_count(chat_id, db, current_user)
    