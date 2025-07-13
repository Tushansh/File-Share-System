from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    user_type = Column(String)  # "ops" or "client"

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    filepath = Column(String)
    uploader_id = Column(Integer, ForeignKey("users.id"))
