"""
Gods Ping Database Models
Simplified schema for single-page trading app
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class User(Base):
    """User model - Admin + 1 additional user"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Encrypted API credentials
    binance_api_key = Column(String, nullable=True)
    binance_api_secret = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    trades = relationship("Trade", back_populates="user")
    bot_config = relationship("BotConfig", back_populates="user", uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'has_api_keys': bool(self.binance_api_key and self.binance_api_secret),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Trade(Base):
    """Trade records"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    symbol = Column(String, index=True)
    side = Column(String)  # BUY or SELL
    amount = Column(Float)
    price = Column(Float)
    filled_price = Column(Float, nullable=True)
    status = Column(String, default="pending")
    bot_type = Column(String, nullable=True)  # 'grid', 'dca', 'gods_hand', 'manual'
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    user = relationship("User", back_populates="trades")


class BotConfig(Base):
    """Unified bot configuration per user"""
    __tablename__ = "bot_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    
    # Trading Settings
    symbol = Column(String, default="BTC/USDT")
    fiat_currency = Column(String, default="USD")  # USD or THB
    budget = Column(Float, default=10000.0)
    paper_trading = Column(Boolean, default=True)
    
    # Risk Management
    risk_level = Column(String, default='moderate')  # conservative, moderate, aggressive
    min_confidence = Column(Float, default=0.7)
    position_size_ratio = Column(Float, default=0.95)
    max_daily_loss = Column(Float, default=5.0)
    
    # Grid Bot Settings
    grid_enabled = Column(Boolean, default=False)
    grid_lower_price = Column(Float, nullable=True)
    grid_upper_price = Column(Float, nullable=True)
    grid_levels = Column(Integer, default=10)
    
    # DCA Bot Settings
    dca_enabled = Column(Boolean, default=False)
    dca_amount_per_period = Column(Float, nullable=True)
    dca_interval_days = Column(Integer, default=1)
    
    # Gods Hand Settings
    gods_hand_enabled = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="bot_config")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'fiat_currency': self.fiat_currency,
            'budget': self.budget,
            'paper_trading': self.paper_trading,
            'risk_level': self.risk_level,
            'min_confidence': self.min_confidence,
            'position_size_ratio': self.position_size_ratio,
            'max_daily_loss': self.max_daily_loss,
            'grid_enabled': self.grid_enabled,
            'grid_lower_price': self.grid_lower_price,
            'grid_upper_price': self.grid_upper_price,
            'grid_levels': self.grid_levels,
            'dca_enabled': self.dca_enabled,
            'dca_amount_per_period': self.dca_amount_per_period,
            'dca_interval_days': self.dca_interval_days,
            'gods_hand_enabled': self.gods_hand_enabled,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
