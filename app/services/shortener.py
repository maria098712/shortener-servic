import random
import string
from sqlalchemy.exc import IntegrityError
from app.database.repositories.links_repo import LinksRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import BASE_URL


class Shortener:

    def __init__(self, links_repo: LinksRepository ) -> None:

        self._links_repo = links_repo

        self._BASE_URL = BASE_URL

    async def shorten(self, original_link: str) -> str:

        original_link = self._http_check(original_link)

        short_key = self._generate_random_string()  # Get short link

        try:
            short_link = self._compose_url(short_key)

            await self._links_repo.add_link(original_link, short_key)

            return short_link

        except IntegrityError:  # Collision protection

            return await self.shorten(original_link)

    def _compose_url(self, short_key) -> str:

        short_link = self._BASE_URL + short_key

        return short_link


    @staticmethod
    def _generate_random_string() -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))  # k = length

    # This for FastApi can redirect normally
    @staticmethod
    def _http_check (original_link: str) -> str:

        if original_link[0:4] == "http":
            return original_link

        else:
            # If possible -> http will automatically become https
            return "http://" + original_link











