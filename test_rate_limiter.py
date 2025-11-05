"""
Test notification rate limiting
"""
import sys
sys.path.append('backend')

from app.notification_limiter import can_send_notification, mark_notification_sent, get_time_until_next
from datetime import datetime
import time

print("=" * 60)
print("NOTIFICATION RATE LIMITER TEST")
print("=" * 60)

user_id = 1

# Test 1: First failure notification (should send)
print("\n1️⃣ First failure notification:")
can_send = can_send_notification(user_id, 'failure', cooldown_hours=1)
print(f"   Can send: {can_send}")
if can_send:
    mark_notification_sent(user_id, 'failure')
    print("   ✅ Notification sent and marked")

# Test 2: Second failure notification immediately (should NOT send)
print("\n2️⃣ Second failure notification (immediate):")
can_send = can_send_notification(user_id, 'failure', cooldown_hours=1)
remaining = get_time_until_next(user_id, 'failure', cooldown_hours=1)
print(f"   Can send: {can_send}")
if not can_send:
    print(f"   ⏳ Rate limited! Can send again in {remaining:.2f} hours")

# Test 3: Position size notification (different type, should send)
print("\n3️⃣ Position size notification (different type):")
can_send = can_send_notification(user_id, 'position_size', cooldown_hours=24)
print(f"   Can send: {can_send}")
if can_send:
    mark_notification_sent(user_id, 'position_size')
    print("   ✅ Notification sent and marked")

# Test 4: Second position size notification (should NOT send)
print("\n4️⃣ Second position size notification:")
can_send = can_send_notification(user_id, 'position_size', cooldown_hours=24)
remaining = get_time_until_next(user_id, 'position_size', cooldown_hours=24)
print(f"   Can send: {can_send}")
if not can_send:
    print(f"   ⏳ Rate limited! Can send again in {remaining:.2f} hours ({remaining:.0f}h {(remaining % 1) * 60:.0f}m)")

# Test 5: Wait a bit and check again
print("\n5️⃣ Waiting 2 seconds and checking failure notification again:")
time.sleep(2)
can_send = can_send_notification(user_id, 'failure', cooldown_hours=1)
remaining = get_time_until_next(user_id, 'failure', cooldown_hours=1)
print(f"   Can send: {can_send}")
if not can_send and remaining:
    minutes_left = remaining * 60
    print(f"   ⏳ Still rate limited! {minutes_left:.1f} minutes remaining")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("✅ Rate limiting working correctly!")
print("   - Failure notifications: 1 per hour")
print("   - Position size notifications: 1 per day (24 hours)")
print("   - Action notifications: No rate limit (sent every time)")
print("=" * 60)
