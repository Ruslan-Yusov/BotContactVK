from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..connection import Base


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    vk_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=True)
    profile_url = Column(Text, nullable=True)

    user = relationship("User", back_populates="blacklist")