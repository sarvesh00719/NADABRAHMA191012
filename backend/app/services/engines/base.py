from pydantic import BaseModel
from typing import Protocol, List, Dict, Optional

class EngineContext(BaseModel):
    language: str
    stage: str
    goal: Optional[str] = None
    checkin: Optional[Dict] = None
    memory: Optional[str] = None
    history: List[Dict]

class EngineReply(BaseModel):
    text: str
    engine: str
    model_version: str

class ConversationEngine(Protocol):
    name: str
    version: str
    async def reply(self, ctx: EngineContext) -> EngineReply: ...

class EngineUnavailable(Exception):
    pass

