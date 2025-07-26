from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import ChatMemberCreate, ChatMemberRead
from app.services import ChatMemberService, ChatService, UserService
from app.models import Chat, User, ChatMember
from app.utils.auth import get_current_user
from app.utils.exceptions import PermissionDeniedError, NotFoundError, AlreadyExistsError

router = APIRouter(prefix="/chat_member", tags=["chat_member"])

@router.post("/join", response_model=ChatMemberRead)
async def add_user_to_chat(user_id: int, chat_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await ChatMemberService.add_user_to_chat(user_id, chat_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except AlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user-memberships/{user_id}", response_model=list[ChatMemberRead])
async def get_chat_memberships(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await ChatMemberService.get_chat_members_by_user_id(user_id, db)

@router.get("/chat-members/{chat_id}", response_model=list[ChatMemberRead])
async def get_chat_members(chat_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await ChatMemberService.get_chat_members_by_chat_id(chat_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/remove-member")
async def remove_member(user_id: int, chat_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try: #I'll refactor the other routes to catch the exceptions from the services soon
        return await ChatMemberService.remove_member(user_id, chat_id, db, current_user)
    except PermissionDeniedError as e: 
        raise HTTPException(status_code=403, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
