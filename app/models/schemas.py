import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.entities import UserRole


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str | None = Field(default=None, pattern=r"^\+?[1-9]\d{1,14}$", description="Valid phone number format")
    password: str = Field(
        min_length=8, 
        max_length=128, 
        description="Password must contain an uppercase, lowercase, number, and special character"
    )
    role: UserRole = UserRole.USER

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[@$!%*?&#]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str | None = None
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    language: Literal["en", "hi"] = "en"
    session_id: int | None = None


class ChatResponse(BaseModel):
    session_id: int
    answer: str
    confidence: float
    sources: list[str]
    escalated: bool


class ChatHistoryRead(BaseModel):
    id: int
    question: str
    answer: str
    confidence: float
    sources: list[str]
    escalated: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatSessionCreate(BaseModel):
    title: str | None = Field(default=None, max_length=255)


class ChatSessionRead(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0


class NotificationRead(BaseModel):
    id: int
    title: str
    body: str
    link: str | None = None
    type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificationBulkAction(BaseModel):
    ids: list[int] = Field(default_factory=list)


class ChatMessageRead(BaseModel):
    id: int
    question: str
    answer: str
    confidence: float
    sources: list[str]
    escalated: bool
    created_at: datetime


class UploadResponse(BaseModel):
    document_id: int
    filename: str
    chunk_count: int
    message: str


class ExpertRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    reason: str = Field(default="manual_request", max_length=255)


class ExpertResolveRequest(BaseModel):
    expert_response: str = Field(min_length=2)
    status: str = Field(default="resolved", max_length=50)


class ExpertQueryRead(BaseModel):
    id: int
    user_id: int
    question: str
    reason: str
    status: str
    expert_response: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GrievanceCreate(BaseModel):
    complaint: str = Field(min_length=5, max_length=5000)


class GrievanceCommentCreate(BaseModel):
    message: str = Field(min_length=1, max_length=3000)


class GrievanceCommentRead(BaseModel):
    id: int
    grievance_id: int
    user_id: int
    message: str
    comment_type: str
    created_at: datetime
    username: str | None = None
    role: UserRole | None = None

    model_config = ConfigDict(from_attributes=True)


class GrievanceRead(BaseModel):
    id: int
    user_id: int
    complaint: str
    status: str
    created_at: datetime
    comments: list[GrievanceCommentRead] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class GrievanceStatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=50)


class GrievanceAdminRead(GrievanceRead):
    username: str | None = None
    email: EmailStr | None = None


class FeedbackCreate(BaseModel):
    question: str
    answer: str
    rating: int = Field(ge=1, le=5)


class FeedbackRead(BaseModel):
    id: int
    question: str
    answer: str
    rating: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionsAnalytics(BaseModel):
    total_questions: int
    escalated_questions: int
    recent_questions: list[dict]


class FailureAnalytics(BaseModel):
    failed_answers: int
    expert_queue_size: int
    unresolved_grievances: int


class UsageAnalytics(BaseModel):
    total_users: int
    total_documents: int
    total_feedback_entries: int
    average_feedback_rating: float
