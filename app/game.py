# app/game.py
from sqlalchemy.orm import Session
from . import models
from datetime import datetime
import random

def resolve_submission(submission_id: int, db: Session):
    """Resolve a submission after voting completes"""
    submission = db.query(models.Submission).filter(
        models.Submission.id == submission_id
    ).first()
    
    # Count votes
    votes = db.query(models.Vote).filter(
        models.Vote.submission_id == submission_id
    ).all()
    
    yes_votes = sum(1 for v in votes if v.vote)
    
    # Determine winner (delulu wins if ≥4 yes votes)
    winning_type = "delulu" if yes_votes >= 4 else "lu"
    
    # Get all bets
    bets = db.query(models.Bet).filter(
        models.Bet.submission_id == submission_id
    ).all()
    
    # Calculate pools
    lu_pool = sum(b.amount for b in bets if b.bet_type == "lu")
    delulu_pool = sum(b.amount for b in bets if b.bet_type == "delulu")
    
    winning_pool = delulu_pool if winning_type == "delulu" else lu_pool
    losing_pool = lu_pool if winning_type == "delulu" else delulu_pool
    
    # Distribute winnings (5% house fee)
    distributable = losing_pool * 0.95
    
    winners = [b for b in bets if b.bet_type == winning_type]
    
    for bet in winners:
        # Proportional payout
        payout = bet.amount + (bet.amount / winning_pool) * distributable
        user = db.query(models.User).filter(
            models.User.telegram_id == bet.user_id
        ).first()
        user.lu_balance += int(payout)
        
        # Record transaction
        transaction = models.Transaction(
            user_id=bet.user_id,
            amount=int(payout - bet.amount),
            type="win",
            reference_id=submission_id
        )
        db.add(transaction)
    
    # Update submission status
    submission.status = "resolved"
    db.commit()
    
    return {"winning_type": winning_type, "winners": len(winners)}

def select_voters(submission_id: int, db: Session, count: int = 7):
    """Select random voters who didn't bet"""
    # Get all users who didn't bet on this submission
    bettors = db.query(models.Bet.user_id).filter(
        models.Bet.submission_id == submission_id
    ).all()
    bettor_ids = [b[0] for b in bettors]
    
    eligible_voters = db.query(models.User).filter(
        ~models.User.telegram_id.in_(bettor_ids)
    ).all()
    
    # Randomly select
    selected = random.sample(eligible_voters, min(count, len(eligible_voters)))
    
    return [v.telegram_id for v in selected]
