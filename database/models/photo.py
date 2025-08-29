from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.connection import Base

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, index=True)
    search_result_id = Column(Integer, ForeignKey('search_results.id', ondelete="CASCADE"), nullable=False)
    photo_url = Column(Text, nullable=False)
    likes = Column(Integer, nullable=False)

    search_result = relationship("SearchResult", back_populates="photos")
