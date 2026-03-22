from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from app.config import settings

DB_URL = settings.DB_URL
engine = create_async_engine(DB_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db

        finally:
            await db.close()