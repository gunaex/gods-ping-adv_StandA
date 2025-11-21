from sqlalchemy.orm import sessionmaker
from app.db import engine
from app.logging_models import Log, LogLevel
from datetime import datetime, timedelta

Session = sessionmaker(bind=engine)

s = Session()
try:
    print('Recent logs for gods_hand (last 100):')
    rows = s.query(Log).filter(Log.bot_type == 'gods_hand').order_by(Log.timestamp.desc()).limit(100).all()
    for r in rows:
        d = r.to_dict()
        # Show only important fields and trim details length
        details = (d['details'][:500] + '...') if d['details'] and len(d['details'])>500 else d['details']
        print(f"[{d['timestamp']}] {d['level'].upper():7} {d['category']:12} {d['message']}")
        if details:
            print('  details:', details)
        if d.get('ai_recommendation') or d.get('execution_reason'):
            print('  ai:', d.get('ai_recommendation'), d.get('ai_confidence'), 'executed=', d.get('ai_executed'), 'reason=', d.get('execution_reason'))
    
    print('\nWarnings or Errors (last 30 days):')
    cutoff = datetime.utcnow() - timedelta(days=30)
    errs = s.query(Log).filter(Log.bot_type=='gods_hand', Log.level.in_([LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]), Log.timestamp >= cutoff).order_by(Log.timestamp.desc()).all()
    for e in errs:
        de = e.to_dict()
        print(f"[{de['timestamp']}] {de['level'].upper():7} {de['category']:12} {de['message']}")
        if de['details']:
            print('  details:', de['details'][:500])

finally:
    s.close()
