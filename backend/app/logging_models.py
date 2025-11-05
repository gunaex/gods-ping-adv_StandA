"""
Comprehensive Logging System for Gods Ping
Categorized logging with database persistence
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum
from datetime import datetime
from app.db import Base
import enum


class LogCategory(str, enum.Enum):
    """Log categories for different types of events"""
    ERROR = "error"                    # System errors, exceptions
    USER = "user"                      # User actions (login, settings changes)
    AI_THINKING = "ai_thinking"        # AI analysis and decision-making process
    AI_ACTION = "ai_action"            # AI actual actions taken
    TRADING = "trading"                # Trade executions, orders
    CONFIG = "config"                  # Configuration changes
    BOT = "bot"                        # Bot operations (Grid, DCA, Gods Hand)
    MARKET = "market"                  # Market data updates, errors
    SYSTEM = "system"                  # System events, startup, shutdown


class LogLevel(str, enum.Enum):
    """Log severity levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Log(Base):
    """Application log entries"""
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    category = Column(SQLEnum(LogCategory), index=True, nullable=False)
    level = Column(SQLEnum(LogLevel), default=LogLevel.INFO, index=True)
    
    # Log content
    message = Column(Text, nullable=False)
    details = Column(Text, nullable=True)  # JSON string with additional data
    
    # Context
    user_id = Column(Integer, nullable=True, index=True)
    symbol = Column(String, nullable=True)
    bot_type = Column(String, nullable=True)
    
    # AI specific fields
    ai_recommendation = Column(String, nullable=True)  # BUY, SELL, HOLD
    ai_confidence = Column(String, nullable=True)
    ai_executed = Column(String, nullable=True)  # "yes", "no", "skipped"
    execution_reason = Column(Text, nullable=True)  # Why action was/wasn't taken
    
    def to_dict(self):
        # Ensure timestamp is explicitly UTC for proper client-side conversion
        timestamp_str = None
        if self.timestamp:
            # Add 'Z' suffix to indicate UTC timezone
            timestamp_str = self.timestamp.isoformat() + 'Z' if not self.timestamp.isoformat().endswith('Z') else self.timestamp.isoformat()
        
        return {
            'id': self.id,
            'timestamp': timestamp_str,
            'category': self.category.value if self.category else None,
            'level': self.level.value if self.level else None,
            'message': self.message,
            'details': self.details,
            'user_id': self.user_id,
            'symbol': self.symbol,
            'bot_type': self.bot_type,
            'ai_recommendation': self.ai_recommendation,
            'ai_confidence': self.ai_confidence,
            'ai_executed': self.ai_executed,
            'execution_reason': self.execution_reason
        }
