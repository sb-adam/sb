from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base, db
from api.models.profiles import Profile
from api.models.user_roles import UserRole

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_banned = Column(Boolean, default=False)
    content = relationship("Content", back_populates="user")

    comments = relationship("Comment", back_populates="user")

    profile = relationship("Profile", uselist=False, back_populates="user")
    user_roles = relationship("UserRole", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'

    def ban(self):
        self.is_banned = True

    def save(self):
        """
        Saves the user to the database.
        """
        db.session.add(self)
        db.session.commit()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
