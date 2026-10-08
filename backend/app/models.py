from sqlalchemy import Column, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base
import uuid

def gen_id():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=gen_id)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    locale = Column(String, default="en")
    status = Column(String, default="active")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    preferences = relationship("Preferences", back_populates="user", uselist=False, cascade="all, delete-orphan")
    check_ins = relationship("CheckIn", back_populates="user", cascade="all, delete-orphan")

class Preferences(Base):
    __tablename__ = "preferences"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    language = Column(String, default="en")
    interaction_mode = Column(String, default="text")
    needs = Column(JSON, default=list)
    retention = Column(String, default="keep")
    onboarding_done = Column(Boolean, default=False)

    user = relationship("User", back_populates="preferences")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False)
    target = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class CheckIn(Base):
    __tablename__ = "check_ins"
    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    mood = Column(String, nullable=False)
    energy = Column(String, nullable=False)
    need = Column(String, nullable=False)
    note = Column(String)

    user = relationship("User", back_populates="check_ins")

class ActivityEvent(Base):
    __tablename__ = "activity_events"
    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String, nullable=True, index=True)
    activity_key = Column(String, nullable=False)
    action = Column(String, nullable=False) # start, complete, skip
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String, nullable=False, index=True)
    choice = Column(String, nullable=False) # helpful, neutral, not_helpful
    comment = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(String, primary_key=True, default=gen_id)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(String, default="active") # active, ended, reviewed
    language = Column(String, default="en")
    goal = Column(String)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)
    retention = Column(String, default="keep")
    crisis_flag = Column(Boolean, default=False)
    
    user = relationship("User")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    review = relationship("SessionReview", back_populates="session", uselist=False, cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True, default=gen_id)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    client_message_id = Column(String, nullable=True, index=True)
    role = Column(String, nullable=False) # user or assistant
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    engine = Column(String, nullable=True)
    model_version = Column(String, nullable=True)
    safety_route = Column(String, default="normal")
    
    session = relationship("SessionModel", back_populates="messages")

class SessionReview(Base):
    __tablename__ = "session_reviews"
    id = Column(String, primary_key=True, default=gen_id)
    session_id = Column(String, ForeignKey("sessions.id"), unique=True, nullable=False)
    draft_summary = Column(String)
    final_summary = Column(String)
    topics = Column(JSON, default=list)
    reflection = Column(String)
    reviewed_at = Column(DateTime, nullable=True)
    
    session = relationship("SessionModel", back_populates="review")

class RagaHandoff(Base):
    __tablename__ = 'raga_handoffs'
    id = Column(String, primary_key=True, default=gen_id)
    session_id = Column(String, ForeignKey('sessions.id'), nullable=False, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    payload = Column(JSON, nullable=False)
    mode = Column(String, nullable=False)
    status = Column(String, default='sent')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
