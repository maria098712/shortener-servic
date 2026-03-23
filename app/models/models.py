from app.models.base import Base
from sqlalchemy import Column, Integer, String, Text, BigInteger


class Link(Base):
    __tablename__ = 'links'

    link_id = Column(Integer, primary_key=True, index=True)
    original_link = Column(Text, nullable=False)
    short_key = Column(String(6), unique=True, nullable=False)
    clicks = Column(BigInteger, default=0)
