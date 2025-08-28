from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from connection import Base

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


class SearchResult(Base):
    __tablename__ = 'search_results'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    vk_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(255), nullable=True)
    profile_url = Column(Text, nullable=True)

    user = relationship("User", back_populates="search_results")
    photos = relationship("Photo", back_populates="search_result", cascade="all, delete-orphan")

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    search_result_id = Column(Integer, ForeignKey('search_results.id', ondelete="CASCADE"), nullable=False)
    photo_url = Column(Text, nullable=False)
    likes = Column(Integer, nullable=False)

    search_result = relationship("SearchResult", back_populates="photos")

class FavoriteUser(Base):
    __tablename__ = 'favorite_users'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    vk_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=True)
    profile_url = Column(Text, nullable=True)

    user = relationship("User", back_populates="favorites")

class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    vk_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=True)
    profile_url = Column(Text, nullable=True)

    user = relationship("User", back_populates="blacklist")
