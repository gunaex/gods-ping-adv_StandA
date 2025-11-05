# Email Notification Rate Limiting - Implementation Summary

## ✅ What's Implemented

### Rate Limiting Rules:
1. **AI Buy/Sell Actions**: ✅ NO rate limit (sent every time)
2. **Position Size Ratio Reached**: ✅ Once per 24 hours (1 day)
3. **AI Failure/Skipped Action**: ✅ Once per 1 hour

### How It Works:

#### `notification_limiter.py`
- Tracks when each notification type was last sent per user
- `can_send_notification(user_id, notification_type, cooldown_hours)` - Checks if enough time has passed
- `mark_notification_sent(user_id, notification_type)` - Records when notification was sent
- `get_time_until_next(user_id, notification_type, cooldown_hours)` - Shows remaining time

#### `bots.py` Updates
- Imports rate limiter functions
- Updated `maybe_send_notification()` helper to accept rate limiting parameters
- Applied rate limits to appropriate notifications:
  - **Failure notifications** (low confidence, position limit, HOLD): 1 hour cooldown
  - **Position size notifications**: 24 hour cooldown
  - **Action notifications** (BUY/SELL): No cooldown (always sent)

### Notification Types and Cooldowns:

```python
# Failure/Skipped Action (3 scenarios, all share same 1-hour cooldown):
maybe_send_notification(
    ...,
    notification_type='failure',
    cooldown_hours=1  # Once per hour
)

# Position Size Ratio Reached:
maybe_send_notification(
    ...,
    notification_type='position_size',
    cooldown_hours=24  # Once per day
)

# Buy/Sell Actions (no rate limit):
if config.notification_email and config.notify_on_action:
    subject, body = format_trade_email(...)
    send_gmail(...)  # Sent immediately every time
```

### User Experience:

1. **First failure**: Email sent immediately ✅
2. **Second failure** (within 1 hour): Skipped with log message ⏳
3. **Third failure** (after 1 hour): Email sent again ✅

4. **Position ratio reached**: Email sent ✅
5. **Position ratio reached again** (within 24 hours): Skipped ⏳
6. **Position ratio reached** (after 24 hours): Email sent again ✅

7. **Every BUY/SELL action**: Email sent (no limit) ✅✅✅

### Console Output:
When rate limited, you'll see:
```
⏳ Notification 'failure' rate limited. Can send again in 0.8 hours
⏳ Notification 'position_size' rate limited. Can send again in 23.5 hours
```

### Storage:
- Rate limiting uses in-memory cache (`_notification_cache`)
- Resets when server restarts (by design, prevents spam on restart)
- For production: Consider using Redis for persistent rate limiting across restarts

### Testing:
- Run `python test_rate_limiter.py` to see rate limiting in action
- Tests all three notification types
- Shows remaining time until next notification

## Frontend Labels (Already Correct):
✅ "Notify when AI buys or sells (multiple times)"
✅ "Notify when Position Size Ratio is reached (once per day)"
✅ "Notify when AI failure/skipped action (once per hour)"

## Benefits:
- ✅ Prevents email spam
- ✅ Still get important action notifications immediately
- ✅ Consolidated failure notifications (won't get 60 emails in an hour)
- ✅ Daily reminder when position target reached
- ✅ Clear console feedback when rate limited
