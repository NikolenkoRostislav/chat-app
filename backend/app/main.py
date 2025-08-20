from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import socketio
from app.config import settings
from app.db import engine, Base
from app.middleware.logging import setup_logging
from app.models import *
from app.api import *
from app.utils.exceptions import *
from app.utils.sockets import sio

app = FastAPI()
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(chat_member_router)
app.include_router(message_router)

@app.exception_handler(InvalidEntryError)
async def invalid_entry_handler(request: Request, exc: InvalidEntryError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(PermissionDeniedError)
async def permission_denied_handler(request: Request, exc: PermissionDeniedError):
    return JSONResponse(status_code=403, content={"detail": str(exc)})

@app.exception_handler(AlreadyExistsError)
async def already_exists_handler(request: Request, exc: AlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

origins = settings.ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_logging(app)

socket_app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path="ws/socket.io")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
