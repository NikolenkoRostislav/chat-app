from contextlib import asynccontextmanager
from app.db.database import SessionLocal

@asynccontextmanager
async def get_db():
    async with SessionLocal() as session:
        yield session
