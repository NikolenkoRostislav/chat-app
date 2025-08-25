from fastapi import APIRouter
from app.schemas import ChatCreate, ChatRead, ChatMemberRead
from app.services import ChatService
from app.utils.exceptions import handle_exceptions
from app.db import DatabaseDep
from app.utils.auth import CurrentUserDep

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatRead)
@handle_exceptions
async def create_chat(chat: ChatCreate, db: DatabaseDep, current_user: CurrentUserDep):
    return await ChatService.create_chat(chat, db, current_user)

@router.get("/{chat_id}", response_model=ChatRead)
@handle_exceptions
async def get_chat(chat_id: int, db: DatabaseDep):
    return await ChatService.get_chat_by_id(chat_id, db, True) 

@router.get("/members/{chat_id}", response_model=list[ChatMemberRead])
@handle_exceptions
async def get_chat_members(chat_id: int, db: DatabaseDep, current_user: CurrentUserDep):
    return await ChatService.get_chat_members_by_chat_id(chat_id, db, current_user)

@router.get("/member-count/{chat_id}")
@handle_exceptions
async def get_chat_member_count(chat_id: int, db: DatabaseDep, current_user: CurrentUserDep):
    return await ChatService.get_chat_member_count(chat_id, db, current_user)

@router.delete("/delete/{chat_id}")
@handle_exceptions
async def delete_chat(chat_id: int, db: DatabaseDep, current_user: CurrentUserDep):
    return await ChatService.delete_chat(chat_id, db, current_user)
    