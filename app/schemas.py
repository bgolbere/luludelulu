from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubmissionCreate(BaseModel):
    content: str
    context: str

class SubmissionResponse(BaseModel):
    id: int
    content: str
    context: str
    status: str
    created_at: datetime
    lu_bets: int = 0
    delulu_bets: int = 0
    
    class Config:
        from_attributes = True

class BetCreate(BaseModel):
    submission_id: int
    bet_type: str  # 'lu' or 'delulu'
    amount: int

class VoteCreate(BaseModel):
    submission_id: int
    vote: bool

class UserResponse(BaseModel):
    telegram_id: int
    username: Optional[str]
    lu_balance: int
    
    class Config:
        from_attributes = True
