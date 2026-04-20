from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    bio: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr
    bio: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    content: str


class PostOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str


class LikeResponse(BaseModel):
    message: str
    post_id: int


class FollowResponse(BaseModel):
    message: str
    target_user_id: int


class UserProfileResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: EmailStr
    bio: Optional[str]
    followers_count: int
    following_count: int
    posts_count: int

    class Config:
        from_attributes = True