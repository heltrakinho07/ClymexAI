"""
CLYMEX AI - Authentication & RBAC Models
"Predict Risk. Protect Tomorrow."
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    INSTITUTION = "INSTITUTION"
    VIEWER = "VIEWER"


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    organization: str
    role: UserRole = UserRole.VIEWER
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: str
    created_at: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    full_name: str
    organization: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None
