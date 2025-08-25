from fastapi import APIRouter
from app.schemas import ChatMemberCreate, ChatMemberDelete, ChatMemberRead
from app.services import ChatMemberService
from app.utils.exceptions import handle_exceptions
from app.db import DatabaseDep
from app.utils.auth import CurrentUserDep

router = APIRouter(prefix="/chat-member", tags=["chat_member"])

@router.post("/join", response_model=ChatMemberRead)
@handle_exceptions
async def add_user_to_chat(chat_member_data: ChatMemberCreate, db: DatabaseDep, current_user: CurrentUserDep):
    return await ChatMemberService.add_user_to_chat(chat_member_data, db, current_user)

@router.patch("/update-status/{chat_member_id}", response_model=ChatMemberRead)
@handle_exceptions
async def update_chat_member_status(chat_member_id: int, is_admin: bool, db: DatabaseDep, current_user: CurrentUserDep):
    return await ChatMemberService.update_chat_member_status(chat_member_id, is_admin, db, current_user)

@router.delete("/remove-member")
@handle_exceptions
async def remove_member(chat_member_data: ChatMemberDelete, db: DatabaseDep, current_user: CurrentUserDep):
    return await ChatMemberService.remove_member(chat_member_data, db, current_user)
