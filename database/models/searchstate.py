from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime

class SearchState(Base):
    __tablename__ = 'search_state'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    last_viewed_vk_id = Column(Integer, nullable=True)
    search_offset = Column(Integer, default=0)
    search_params = Column(String(500), nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
