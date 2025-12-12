from datetime import datetime, timedelta
import schedule
import threading
import time
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.orm import URL

def delete_expired(session_factory, ttl_minutes: int) -> None:
    now = datetime.now()
    cutoff = now - timedelta(minutes=ttl_minutes)
    session: Session = session_factory()
    try:
        stmt = delete(URL).where(URL.created_at < cutoff)
        result = session.execute(stmt)
        session.commit()
        return result.rowcount if hasattr(result, "rowcount") else 0
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def _run_loop(stop_event):
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)

def start_background_scheduler(session_factory, ttl_minutes: int, every_minutes: int = 10):
    schedule.clear('url_cleanup')
    schedule.every(every_minutes).minutes.do(
        lambda: delete_expired(session_factory, ttl_minutes)
    ).tag('url_cleanup')

    stop_event = threading.Event()
    t = threading.Thread(target=_run_loop, args=(stop_event,), daemon=True)
    t.start()
    return stop_event
