from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

class CommentModeration(Base):
    __tablename__ = "comment_moderation"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)
    moderator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    comment = relationship("Comment", back_populates="moderation")
    moderator = relationship("User", back_populates="moderated_comments")

    def __repr__(self):
        return f"<CommentModeration id={self.id} comment_id={self.comment_id} moderator_id={self.moderator_id}>"
