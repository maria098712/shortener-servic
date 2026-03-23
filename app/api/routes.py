from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException
from app.database.repositories.links_repo import LinksRepository
from app.schemas.schemas import (CreateShortLinkRequest,
                                 CreateShortLinkResponse,
                                 GetLinkHitsResponse)

from app.services.shortener import Shortener
from app.dependencies.shortener_factory import get_shortener, get_links_repo
from fastapi import Request


router = APIRouter()


# Get short link
@router.post("/shorten", response_model=CreateShortLinkResponse)
async def shorten_link(link: CreateShortLinkRequest,
                       shortener: Shortener = Depends(get_shortener)):

    short_link = await shortener.shorten(link.original_link)

    return CreateShortLinkResponse(short_link=short_link)


# Service endpoint (redirect user on original link)
@router.get("/{short_id}", response_class=RedirectResponse)
async def redirect_user(request: Request,
                        links_repo: LinksRepository = Depends(get_links_repo)):

    short_key = request.path_params["short_id"]

    redirect_link = await links_repo.get_redirect_link(short_key)

    if not redirect_link:
        raise HTTPException(status_code=404)

    await links_repo.increase_click(short_key)

    return RedirectResponse(url=redirect_link)


# Get number of hits on a link
@router.get("/stats/{short_id}", response_model=GetLinkHitsResponse)
async def get_links_stats(request: Request, short_id: str,
                          links_repo: LinksRepository = Depends(get_links_repo)):

    link_clicks = await links_repo.get_link_stats(short_id)

    if not link_clicks:
        raise HTTPException(status_code=404)

    return {
        "link_clicks": link_clicks,
    }
















