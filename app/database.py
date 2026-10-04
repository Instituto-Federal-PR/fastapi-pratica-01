import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg://post_user:post_pass@db:5432/fastapi_db"
)

# Engine e SessionMaker ASSÍNCRONOS (compatíveis com o psycopg v3)
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

# Dependência do FastAPI para fornecer a sessão assíncrona ao fastapi-users
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        
# Alias para não dar erro nos imports dos endpoints existentes
get_db = get_async_session