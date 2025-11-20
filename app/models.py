from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    lu_balance = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    submissions = relationship("Submission", back_populates="user")
    bets = relationship("Bet", back_populates="user")
    votes = relationship("Vote", back_populates="user")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    content = Column(String, nullable=False)
    context = Column(String, nullable=False)
    status = Column(String, default="betting")  # betting, voting, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
    betting_ends_at = Column(DateTime)
    voting_ends_at = Column(DateTime)
    
    user = relationship("User", back_populates="submissions")
    bets = relationship("Bet", back_populates="submission")
    votes = relationship("Vote", back_populates="submission")

class Bet(Base):
    __tablename__ = "bets"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    bet_type = Column(String)  # 'lu' or 'delulu'
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="bets")
    submission = relationship("Submission", back_populates="bets")

class Vote(Base):
    __tablename__ = "votes"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"))
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    vote = Column(Boolean)  # True = worked, False = didn't
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="votes")
    submission = relationship("Submission", back_populates="votes")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"))
    amount = Column(Integer)
    type = Column(String)  # bet, win, vote_reward, daily_stipend
    reference_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
