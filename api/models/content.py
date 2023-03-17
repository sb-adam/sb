from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(2000))
    content_type = Column(String(50), nullable=False)
    file_url = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="content")
    comments = relationship("Comment", back_populates="content")
    ratings = relationship("Rating", back_populates="content")

    def __repr__(self):
        return f"<Content id={self.id} user_id={self.user_id} title={self.title} content_type={self.content_type}>"
