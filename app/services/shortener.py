import random
import string
from sqlalchemy.exc import IntegrityError
from app.database.repositories.links_repo import LinksRepository
from sqlalchemy.ext.asyncio import AsyncSession


class Shortener:

    def __init__(self, links_repo: LinksRepository ) -> None:

        self.links_repo = links_repo

    async def shorten(self, original_link: str) -> str:

        short_link = self.generate_random_string()  # Get short link

        try:
            await self.links_repo.add_link(original_link, short_link)
            return short_link

        except IntegrityError:  # Collision protection

            return await self.shorten(original_link)


    @staticmethod
    def generate_random_string() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # k = length





