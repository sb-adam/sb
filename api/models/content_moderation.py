from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
import datetime

class ContentModeration(Base):
    __tablename__ = "content_moderation"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("content.id"), nullable=False)
    moderator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(Enum("nothing", "delete", "banned", name="moderation_actions"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    content = relationship("Content", back_populates="moderation")
    moderator = relationship("User", back_populates="moderated_content")

    def __repr__(self):
        return f"<ContentModeration id={self.id} content_id={self.content_id} moderator_id={self.moderator_id} action={self.action}>"
