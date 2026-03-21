from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Link
from app.config import lg


class LinksRepository:

    # Get session
    def __init__(self, db: AsyncSession):
        self._db = db

    # Add new link
    async def add_link(self, original_link: str, short_key: str) -> None:

        stmt = (
            insert(Link)
            .values(original_link=original_link, short_key=short_key, clicks=0)
        )

        try:
            await self._db.execute(stmt)
            await self._db.commit()

        except Exception as error:
            lg.error(f"Error while trying to insert link ->:{error}")
            await self._db.rollback()

    # Get redirect link by short
    async def get_redirect_link(self, short_key: str) -> str:

        stmt = (
            select(Link.original_link)
            .where(Link.short_key == short_key)
        )
        try:
            result = await self._db.execute(stmt)
            redirect_link = result.scalar_one()

            return redirect_link

        except Exception as error:

            lg.error(f"Error while trying to get redirect link ->:{error}")
            await self._db.rollback()
            return ""

    # Increases the number of clicks by 1
    async def increase_click(self, short_key: str) -> None:

        stmt = (
            update(Link)
            .where(Link.short_key == short_key)
            .values(clicks=Link.clicks + 1)
        )

        try:
            await self._db.execute(stmt)
            await self._db.commit()

        except Exception as error:
            lg.error(f"Error while trying to update clicks ->:{error}")
            await self._db.rollback()

    # Get clicks number
    async def  get_link_stats(self, short_key: str) -> int:

        stmt = (
            select(Link.clicks)
            .where(Link.short_key == short_key)
        )

        try:
            result = await self._db.execute(stmt)
            clicks = result.scalar_one()
            return clicks

        except Exception as error:
            lg.error(f"Error while trying to get clicks ->:{error}")
            await self._db.rollback()
            return 0

    # Get short link by short link
    async def get_short_link(self, short_key: str) -> str | None:

        stmt = (
            select(Link.short_key)
            .where(Link.short_key == short_key)
        )

        try:
            result = await self._db.execute(stmt)
            short_link = result.scalar_one()
            return short_link

        except Exception as error:
            lg.error(f"Error while trying to get short link ->:{error}")
            await self._db.rollback()
