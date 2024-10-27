# models.py
from sqlalchemy import Column, Integer, String, ARRAY
from database import Base
from pydantic import BaseModel
from sqlalchemy.ext.mutable import MutableList

class SignupRequest(BaseModel):
    username: str
    password: str

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    downloads = Column(MutableList.as_mutable(ARRAY(String)), default=[])

class DownloadRequest(BaseModel):
    url: str
