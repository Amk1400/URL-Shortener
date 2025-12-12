from datetime import datetime, timedelta
import schedule
import threading
import time
from typing import Callable, Optional
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.models.orm import URL


def delete_expired(session_factory: Callable[[], Session], ttl_minutes: int) -> int:
    """Delete URLs older than TTL.

    Args:
        session_factory (Callable[[], Session]): Session factory callable.
        ttl_minutes (int): Time-to-live in minutes.

    Returns:
        int: Number of rows deleted.

    Raises:
        Exception: On DB errors.
    """
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


def _run_loop(stop_event: threading.Event) -> None:
    """Run schedule loop until stop_event is set.

    Args:
        stop_event (threading.Event): Event to stop loop.

    Returns:
        None

    Raises:
        None
    """
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)


def start_background_scheduler(session_factory: Callable[[], Session], ttl_minutes: int, every_minutes: int = 10):
    """Start background scheduler to remove expired URLs.

    Args:
        session_factory (Callable[[], Session]): Session factory callable.
        ttl_minutes (int): TTL in minutes for expiry.
        every_minutes (int): Interval in minutes to run cleanup.

    Returns:
        threading.Event: Stop event that can be set to stop the scheduler.

    Raises:
        None
    """
    schedule.clear("url_cleanup")
    schedule.every(every_minutes).minutes.do(
        lambda: delete_expired(session_factory, ttl_minutes)
    ).tag("url_cleanup")

    stop_event = threading.Event()
    t = threading.Thread(target=_run_loop, args=(stop_event,), daemon=True)
    t.start()
    return stop_event
