from pydantic import BaseModel


class CreateShortLinkResponse(BaseModel):
    short_link: str

class CreateShortLinkRequest(BaseModel):
    original_link: str

class RedirectUserRequest(BaseModel):
    short_link: str

class GetLinkHitsResponse(BaseModel):
    clicks: int

