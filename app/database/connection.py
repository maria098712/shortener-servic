from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from app.config import settings
from sqlalchemy.pool import NullPool, QueuePool


DB_URL = settings.DB_URL

if settings.MODE == "TEST":
    pool_class = NullPool

else:
    pool_class = QueuePool

engine = create_async_engine(DB_URL, echo=True, poolclass=pool_class)

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