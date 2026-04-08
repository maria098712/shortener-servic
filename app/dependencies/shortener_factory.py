from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.repositories.links_repo import LinksRepository
from app.services.shortener import Shortener


def get_links_repo(db: AsyncSession = Depends(get_db)) -> LinksRepository:
    return LinksRepository(db)


def get_shortener(
        links_repo: LinksRepository = Depends(get_links_repo),
        db: AsyncSession = Depends(get_db)
        ) -> Shortener:
    return Shortener(links_repo, db)
