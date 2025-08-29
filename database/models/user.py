from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    vk_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)
    sex = Column(String(10), nullable=True)

    search_results = relationship("SearchResult", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("FavoriteUser", back_populates="user", cascade="all, delete-orphan")
    blacklist = relationship("Blacklist", back_populates="user", cascade="all, delete-orphan")