from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List

from . import models, schemas
from .database import engine, get_db

# Create all tables
print("Creating database tables...")
models.Base.metadata.create_all(bind=engine)
print("Database tables created!")

app = FastAPI(
    title="luludelulu",
    version="0.1.0",
    description="Bet on whether jokes will land"
)


# CORS for Telegram WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "luludelulu API",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# User endpoints
@app.post("/api/users", response_model=schemas.UserResponse)
async def create_user(
    telegram_id: int,
    username: str = None,
    db: Session = Depends(get_db)
):
    """Create or get user"""
    user = db.query(models.User).filter(
        models.User.telegram_id == telegram_id
    ).first()
    
    if user:
        return user
    
    user = models.User(telegram_id=telegram_id, username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/api/users/{telegram_id}", response_model=schemas.UserResponse)
async def get_user(telegram_id: int, db: Session = Depends(get_db)):
    """Get user by telegram_id"""
    user = db.query(models.User).filter(
        models.User.telegram_id == telegram_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# Submission endpoints
@app.get("/api/submissions", response_model=List[schemas.SubmissionResponse])
async def get_submissions(
    status: str = "betting",
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get submissions by status"""
    submissions = db.query(models.Submission).filter(
        models.Submission.status == status
    ).limit(limit).all()
    
    result = []
    for sub in submissions:
        lu_bets = sum(b.amount for b in sub.bets if b.bet_type == "lu")
        delulu_bets = sum(b.amount for b in sub.bets if b.bet_type == "delulu")
        
        result.append({
            **schemas.SubmissionResponse.model_validate(sub).model_dump(),
            "lu_bets": lu_bets,
            "delulu_bets": delulu_bets,
            "total_bets": len(sub.bets)
        })
    
    return result

@app.post("/api/submissions", response_model=schemas.SubmissionResponse)
async def create_submission(
    submission: schemas.SubmissionCreate,
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """Create new submission (costs 5 Lu)"""
    user = db.query(models.User).filter(
        models.User.telegram_id == telegram_id
    ).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.lu_balance < 5:
        raise HTTPException(status_code=400, detail="Insufficient Lu (need 5)")
    
    # Deduct submission cost
    user.lu_balance -= 5
    
    # Create submission
    new_sub = models.Submission(
        user_id=telegram_id,
        content=submission.content,
        context=submission.context,
        betting_ends_at=datetime.utcnow() + timedelta(hours=24)
    )
    
    db.add(new_sub)
    
    # Record transaction
    transaction = models.Transaction(
        user_id=telegram_id,
        amount=-5,
        type="submission_cost",
        reference_id=None
    )
    db.add(transaction)
    
    db.commit()
    db.refresh(new_sub)
    
    return new_sub

# Betting endpoints
@app.post("/api/bets")
async def place_bet(
    bet: schemas.BetCreate,
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """Place a bet (lu or delulu)"""
    user = db.query(models.User).filter(
        models.User.telegram_id == telegram_id
    ).first()
    
    submission = db.query(models.Submission).filter(
        models.Submission.id == bet.submission_id
    ).first()
    
    if not user or not submission:
        raise HTTPException(status_code=404, detail="Not found")
    
    if user.lu_balance < bet.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient Lu (have {user.lu_balance}, need {bet.amount})"
        )
    
    if bet.amount < 10:
        raise HTTPException(status_code=400, detail="Minimum bet is 10 Lu")
    
    if submission.status != "betting":
        raise HTTPException(status_code=400, detail="Betting closed")
    
    if datetime.utcnow() > submission.betting_ends_at:
        raise HTTPException(status_code=400, detail="Betting period ended")
    
    # Check for existing bet
    existing = db.query(models.Bet).filter(
        models.Bet.user_id == telegram_id,
        models.Bet.submission_id == bet.submission_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already bet on this submission")
    
    # Place bet
    user.lu_balance -= bet.amount
    
    new_bet = models.Bet(
        user_id=telegram_id,
        submission_id=bet.submission_id,
        bet_type=bet.bet_type,
        amount=bet.amount
    )
    db.add(new_bet)
    
    # Record transaction
    transaction = models.Transaction(
        user_id=telegram_id,
        amount=-bet.amount,
        type="bet",
        reference_id=bet.submission_id
    )
    db.add(transaction)
    
    db.commit()
    
    return {
        "status": "success",
        "remaining_balance": user.lu_balance,
        "bet_type": bet.bet_type,
        "amount": bet.amount
    }

@app.get("/api/leaderboard", response_model=List[schemas.UserResponse])
async def get_leaderboard(limit: int = 10, db: Session = Depends(get_db)):
    """Get top Lu holders"""
    users = db.query(models.User).order_by(
        models.User.lu_balance.desc()
    ).limit(limit).all()
    
    return users

@app.post("/api/votes")
async def cast_vote(
    vote: schemas.VoteCreate,
    telegram_id: int,
    db: Session = Depends(get_db)
):
    """Cast a vote on a submission"""
    from .game import cast_vote as game_cast_vote
    return game_cast_vote(telegram_id, vote.submission_id, vote.vote, db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",  # Import string
        host="0.0.0.0",
        port=8000,
        reload=True
    )
