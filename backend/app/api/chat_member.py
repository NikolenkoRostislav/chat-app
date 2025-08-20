from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import ChatMemberCreate, ChatMemberDelete, ChatMemberRead
from app.services import ChatMemberService
from app.models import User, ChatMember
from app.utils.auth import get_current_user
from app.utils.exceptions import handle_exceptions

router = APIRouter(prefix="/chat-member", tags=["chat_member"])

@router.post("/join", response_model=ChatMemberRead)
@handle_exceptions
async def add_user_to_chat(chat_member_data: ChatMemberCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.add_user_to_chat(chat_member_data, db, current_user)

@router.patch("/update-status/{chat_member_id}", response_model=ChatMemberRead)
@handle_exceptions
async def update_chat_member_status(chat_member_id: int, is_admin: bool, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.update_chat_member_status(chat_member_id, is_admin, db, current_user)

@router.delete("/remove-member")
@handle_exceptions
async def remove_member(chat_member_data: ChatMemberDelete, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.remove_member(chat_member_data, db, current_user)
