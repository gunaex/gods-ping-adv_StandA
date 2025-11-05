"""
Email Notification Rate Limiter
Tracks when notifications were last sent to prevent spam
"""
from datetime import datetime, timedelta
from typing import Dict, Optional

# In-memory cache for last notification times
# Structure: {user_id: {notification_type: last_sent_datetime}}
_notification_cache: Dict[int, Dict[str, datetime]] = {}


def can_send_notification(user_id: int, notification_type: str, cooldown_hours: int = 1) -> bool:
    """
    Check if enough time has passed to send a notification.
    
    Args:
        user_id: User ID
        notification_type: Type of notification (e.g., 'failure', 'position_size')
        cooldown_hours: Minimum hours between notifications (default: 1)
        
    Returns:
        True if notification can be sent, False otherwise
    """
    if user_id not in _notification_cache:
        _notification_cache[user_id] = {}
    
    last_sent = _notification_cache[user_id].get(notification_type)
    
    if last_sent is None:
        return True
    
    time_since_last = datetime.utcnow() - last_sent
    cooldown = timedelta(hours=cooldown_hours)
    
    return time_since_last >= cooldown


def mark_notification_sent(user_id: int, notification_type: str):
    """
    Mark that a notification was sent at current time.
    
    Args:
        user_id: User ID
        notification_type: Type of notification
    """
    if user_id not in _notification_cache:
        _notification_cache[user_id] = {}
    
    _notification_cache[user_id][notification_type] = datetime.utcnow()


def get_time_until_next(user_id: int, notification_type: str, cooldown_hours: int = 1) -> Optional[float]:
    """
    Get hours remaining until next notification can be sent.
    
    Returns:
        Hours remaining, or None if can send now
    """
    if user_id not in _notification_cache:
        return None
    
    last_sent = _notification_cache[user_id].get(notification_type)
    if last_sent is None:
        return None
    
    time_since_last = datetime.utcnow() - last_sent
    cooldown = timedelta(hours=cooldown_hours)
    remaining = cooldown - time_since_last
    
    if remaining.total_seconds() <= 0:
        return None
    
    return remaining.total_seconds() / 3600  # Convert to hours
