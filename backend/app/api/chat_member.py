from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import ChatMemberCreate, ChatMemberRead, ChatRead
from app.services import ChatMemberService
from app.models import Chat, User, ChatMember
from app.utils.auth import get_current_user
from app.utils.exceptions import handle_exceptions

router = APIRouter(prefix="/chat-member", tags=["chat_member"])

@router.post("/join", response_model=ChatMemberRead)
@handle_exceptions
async def add_user_to_chat(chat_member_data: ChatMemberCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.add_user_to_chat(chat_member_data, db, current_user)

@router.get("/me", response_model=list[ChatMemberRead])
@handle_exceptions
async def get_chat_memberships(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.get_chat_members_by_user_id(current_user.id, db, current_user)

@router.get("/user-memberships/{chat_id}", response_model=list[ChatMemberRead])
@handle_exceptions
async def get_chat_members(chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.get_chat_members_by_chat_id(chat_id, db, current_user)

@router.get("/user-memberships-count/{chat_id}")
@handle_exceptions
async def get_chat_member_count(chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.get_chat_member_count(chat_id, db, current_user)

@router.get("/chats/me", response_model=list[ChatRead])
@handle_exceptions
async def get_chats_me(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.get_chats_by_current_user(db, current_user)

@router.delete("/remove-member")
@handle_exceptions
async def remove_member(user_id: int, chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.remove_member(user_id, chat_id, db, current_user)

@router.patch("/update-member-status/{chat_member_id}", response_model=ChatMemberRead)
@handle_exceptions
async def update_chat_member_status(chat_member_id: int, is_admin: bool, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatMemberService.update_chat_member_status(chat_member_id, is_admin, db, current_user)
