from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class UserPreferences(BaseModel):
    language: str = "en"
    interaction_mode: str = "text"
    needs: List[str] = Field(default_factory=list)
    retention: str = "keep"
    onboarding_done: bool = False

class UserResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: str
    email: str
    display_name: str
    locale: str

class UserProfileResponse(UserResponse):
    preferences: UserPreferences

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    display_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    preferences: Optional[UserPreferences] = None

class CheckInCreate(BaseModel):
    mood: str
    energy: str
    need: str
    note: Optional[str] = None
    
class CheckInResponse(CheckInCreate):
    model_config = {'from_attributes': True}
    id: str
    created_at: datetime
    
class CheckInListResponse(BaseModel):
    items: List[CheckInResponse]
    trend_available: bool

class ActivityEventCreate(BaseModel):
    activity_key: str
    action: str
    session_id: Optional[str] = None
    
class FeedbackCreate(BaseModel):
    session_id: str
    choice: str
    comment: Optional[str] = None

