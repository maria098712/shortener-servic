from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends
from app.database.repositories.links_repo import LinksRepository
from app.schemas.schemas import CreateShortLinkRequest, CreateShortLinkResponse, GetLinkHitsResponse
from app.services.shortener import Shortener
from app.dependencies.shortener_factory import get_shortener, get_links_repo
from fastapi import FastAPI, Request



router = APIRouter()

@router.post("/shorten", response_model=CreateShortLinkResponse)
async def shorten_link(link: CreateShortLinkRequest, shortener: Shortener = Depends(get_shortener)):

    short_link = await shortener.shorten(link.original_link)

    return CreateShortLinkResponse(short_link=short_link)

@router.get("/{short_id}", response_class=RedirectResponse)
async def redirect_user(request: Request, links_repo: LinksRepository = Depends(get_links_repo)):

    short_key = request.path_params["short_id"]

    redirect_link = await links_repo.get_redirect_link(short_key)

    await links_repo.increase_click(short_key)

    return RedirectResponse(url=redirect_link)

@router.get("/stats/{short_id}", response_model=GetLinkHitsResponse)
async def get_links_stats(request: Request, links_repo: LinksRepository = Depends(get_links_repo)):

    short_key = request.path_params["short_id"]

    link_clicks = await links_repo.get_link_stats(short_key)

    return GetLinkHitsResponse(clicks=link_clicks)

















