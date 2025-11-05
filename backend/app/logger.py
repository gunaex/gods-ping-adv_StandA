"""
Logger Service for Gods Ping
Centralized logging with category support and AI action tracking
"""
from sqlalchemy.orm import Session
from app.logging_models import Log, LogCategory, LogLevel
from datetime import datetime
from typing import Optional
import json


class Logger:
    """Centralized logger for the application"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log(
        self,
        category: LogCategory,
        message: str,
        level: LogLevel = LogLevel.INFO,
        details: Optional[dict] = None,
        user_id: Optional[int] = None,
        symbol: Optional[str] = None,
        bot_type: Optional[str] = None,
        ai_recommendation: Optional[str] = None,
        ai_confidence: Optional[float] = None,
        ai_executed: Optional[str] = None,
        execution_reason: Optional[str] = None
    ):
        """Create a log entry"""
        try:
            log_entry = Log(
                timestamp=datetime.utcnow(),
                category=category,
                level=level,
                message=message,
                details=json.dumps(details) if details else None,
                user_id=user_id,
                symbol=symbol,
                bot_type=bot_type,
                ai_recommendation=ai_recommendation,
                ai_confidence=str(ai_confidence) if ai_confidence else None,
                ai_executed=ai_executed,
                execution_reason=execution_reason
            )
            
            self.db.add(log_entry)
            self.db.commit()
            
            # Also print to console for development
            print(f"[{category.value.upper()}] {message}")
            
            return log_entry
        except Exception as e:
            print(f"Failed to create log entry: {str(e)}")
            self.db.rollback()
    
    # Convenience methods for common log types
    
    def error(self, message: str, details: Optional[dict] = None, **kwargs):
        """Log an error"""
        return self.log(LogCategory.ERROR, message, LogLevel.ERROR, details, **kwargs)
    
    def user_action(self, message: str, user_id: int, details: Optional[dict] = None):
        """Log a user action"""
        return self.log(LogCategory.USER, message, LogLevel.INFO, details, user_id=user_id)
    
    def ai_thinking(
        self,
        message: str,
        symbol: str,
        recommendation: str,
        confidence: float,
        details: Optional[dict] = None,
        user_id: Optional[int] = None
    ):
        """Log AI thinking/analysis process"""
        return self.log(
            LogCategory.AI_THINKING,
            message,
            LogLevel.INFO,
            details,
            user_id=user_id,
            symbol=symbol,
            ai_recommendation=recommendation,
            ai_confidence=confidence
        )
    
    def ai_action(
        self,
        message: str,
        symbol: str,
        recommendation: str,
        executed: bool,
        reason: str,
        confidence: Optional[float] = None,
        details: Optional[dict] = None,
        user_id: Optional[int] = None
    ):
        """Log AI action (whether executed or not)"""
        return self.log(
            LogCategory.AI_ACTION,
            message,
            LogLevel.INFO if executed else LogLevel.WARNING,
            details,
            user_id=user_id,
            symbol=symbol,
            ai_recommendation=recommendation,
            ai_confidence=confidence,
            ai_executed="yes" if executed else "no",
            execution_reason=reason
        )
    
    def trading(self, message: str, symbol: str, details: Optional[dict] = None, user_id: Optional[int] = None):
        """Log trading activities"""
        return self.log(
            LogCategory.TRADING,
            message,
            LogLevel.INFO,
            details,
            user_id=user_id,
            symbol=symbol
        )
    
    def config_change(self, message: str, details: Optional[dict] = None, user_id: Optional[int] = None):
        """Log configuration changes"""
        return self.log(LogCategory.CONFIG, message, LogLevel.INFO, details, user_id=user_id)
    
    def bot_operation(self, message: str, bot_type: str, details: Optional[dict] = None, user_id: Optional[int] = None):
        """Log bot operations"""
        return self.log(
            LogCategory.BOT,
            message,
            LogLevel.INFO,
            details,
            user_id=user_id,
            bot_type=bot_type
        )
    
    def system(self, message: str, level: LogLevel = LogLevel.INFO, details: Optional[dict] = None):
        """Log system events"""
        return self.log(LogCategory.SYSTEM, message, level, details)


def get_logger(db: Session) -> Logger:
    """Get logger instance"""
    return Logger(db)
