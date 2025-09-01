from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..connection import Base

class SearchResult(Base):
    __tablename__ = 'search_results'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    vk_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    profile_url = Column(Text, nullable=True)

    user = relationship("User", back_populates="search_results")
    photos = relationship("Photo", back_populates="search_result", cascade="all, delete-orphan")