from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.models.roles import Role
from ..database import Base, db

class UserRole(db.Model):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    user = relationship("User", back_populates="user_roles")
    role = relationship("Role")

    def __repr__(self):
        return f"<UserRole id={self.id} user_id={self.user_id} role_id={self.role_id}>"
