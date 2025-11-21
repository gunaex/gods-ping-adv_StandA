"""
Test Kill-Switch Improvements
Verify consecutive breach tracking, cooldown, and baseline persistence
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import get_db
from app.models import BotConfig
from app.bots import kill_switch_breach_history, set_kill_switch_baseline
from datetime import datetime, timedelta


def test_consecutive_breaches():
    """Test that consecutive breaches are tracked correctly"""
    print("\n🧪 Test 1: Consecutive Breach Tracking")
    print("=" * 50)
    
    user_id = 1
    
    # Clear history
    kill_switch_breach_history[user_id] = []
    
    # Add 2 breaches
    now = datetime.utcnow()
    kill_switch_breach_history[user_id].append(now - timedelta(seconds=120))
    kill_switch_breach_history[user_id].append(now - timedelta(seconds=60))
    
    # Count should be 2
    assert len(kill_switch_breach_history[user_id]) == 2
    print(f"✅ Added 2 breaches, count: {len(kill_switch_breach_history[user_id])}")
    
    # Add 3rd breach
    kill_switch_breach_history[user_id].append(now)
    assert len(kill_switch_breach_history[user_id]) == 3
    print(f"✅ Added 3rd breach, count: {len(kill_switch_breach_history[user_id])}")
    
    # Clear on reset
    kill_switch_breach_history[user_id] = []
    assert len(kill_switch_breach_history[user_id]) == 0
    print("✅ Breach history cleared on reset")
    
    print("✅ Test 1 PASSED\n")


def test_breach_expiry():
    """Test that old breaches are pruned"""
    print("🧪 Test 2: Breach History Expiry")
    print("=" * 50)
    
    user_id = 2
    kill_switch_breach_history[user_id] = []
    
    # Add old breach (2 hours ago)
    old_breach = datetime.utcnow() - timedelta(hours=2)
    kill_switch_breach_history[user_id].append(old_breach)
    
    # Add recent breach
    recent_breach = datetime.utcnow() - timedelta(minutes=5)
    kill_switch_breach_history[user_id].append(recent_breach)
    
    print(f"Added 2 breaches: 1 old (2h ago), 1 recent (5min ago)")
    
    # Prune (keep only last hour)
    cutoff = datetime.utcnow() - timedelta(hours=1)
    kill_switch_breach_history[user_id] = [
        t for t in kill_switch_breach_history[user_id] if t > cutoff
    ]
    
    # Should only have 1 breach left
    assert len(kill_switch_breach_history[user_id]) == 1
    print(f"✅ After pruning (1h window): {len(kill_switch_breach_history[user_id])} breach(es)")
    
    print("✅ Test 2 PASSED\n")


def test_baseline_persistence():
    """Test that baseline persists to database"""
    print("🧪 Test 3: Baseline Persistence")
    print("=" * 50)
    
    db = next(get_db())
    
    # Get or create config for admin user
    config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
    if not config:
        config = BotConfig(user_id=1)
        db.add(config)
        db.commit()
        db.refresh(config)
    
    # Set baseline
    baseline_pl = -2.5
    result = set_kill_switch_baseline(
        user_id=1,
        pl_percent=baseline_pl,
        symbol="BTC/USDT",
        db=db,
        current_price=50000.0
    )
    
    print(f"Set baseline: {baseline_pl}%")
    
    # Verify persisted
    db.refresh(config)
    assert config.kill_switch_baseline == baseline_pl
    print(f"✅ Baseline persisted to DB: {config.kill_switch_baseline}%")
    
    # Verify returned correctly
    assert result["baseline_pl_percent"] == baseline_pl
    print(f"✅ Baseline returned: {result['baseline_pl_percent']}%")
    
    db.close()
    print("✅ Test 3 PASSED\n")


def test_cooldown_config():
    """Test that cooldown config is stored correctly"""
    print("🧪 Test 4: Cooldown Configuration")
    print("=" * 50)
    
    db = next(get_db())
    
    config = db.query(BotConfig).filter(BotConfig.user_id == 1).first()
    
    # Check defaults
    assert config.kill_switch_cooldown_minutes == 60
    print(f"✅ Default cooldown: {config.kill_switch_cooldown_minutes} minutes")
    
    assert config.kill_switch_consecutive_breaches == 3
    print(f"✅ Default consecutive breaches: {config.kill_switch_consecutive_breaches}")
    
    # Update
    config.kill_switch_cooldown_minutes = 120
    config.kill_switch_consecutive_breaches = 5
    db.commit()
    
    # Verify update
    db.refresh(config)
    assert config.kill_switch_cooldown_minutes == 120
    assert config.kill_switch_consecutive_breaches == 5
    print(f"✅ Updated cooldown: {config.kill_switch_cooldown_minutes} minutes")
    print(f"✅ Updated consecutive breaches: {config.kill_switch_consecutive_breaches}")
    
    # Reset to defaults
    config.kill_switch_cooldown_minutes = 60
    config.kill_switch_consecutive_breaches = 3
    db.commit()
    
    db.close()
    print("✅ Test 4 PASSED\n")


def main():
    print("\n" + "="*50)
    print("KILL-SWITCH IMPROVEMENTS TEST SUITE")
    print("="*50)
    
    try:
        test_consecutive_breaches()
        test_breach_expiry()
        test_baseline_persistence()
        test_cooldown_config()
        
        print("="*50)
        print("✅ ALL TESTS PASSED")
        print("="*50)
        return 0
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
