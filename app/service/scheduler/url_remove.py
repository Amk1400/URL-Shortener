import threading
import time
from typing import Callable, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.orm import Session

import schedule

from app.models.orm import URL


def delete_expired_urls(session_factory: Callable[[], Session]) -> int:
    """
    Delete all URL rows where expired_at is set and expired_at < now().
    Returns number of rows deleted.
    """
    session: Session = session_factory()
    try:
        q = session.query(URL).filter(URL.expired_at != None, URL.expired_at < func.now())
        count = q.count()
        if count > 0:
            q.delete(synchronize_session=False)
            session.commit()
        return count
    except SQLAlchemyError as exc:
        session.rollback()
        raise RuntimeError(f"Database error while deleting expired URLs: {repr(exc)}")
    finally:
        session.close()


class UrlCleanupScheduler:
    """
    Background scheduler using the `schedule` package.

    Usage:
        scheduler = UrlCleanupScheduler(session_factory=db.get_session, interval_seconds=60)
        scheduler.start()
        ...
        scheduler.stop()
    """

    def __init__(self, session_factory: Callable[[], Session], interval_seconds: int = 60):
        if interval_seconds < 1:
            raise ValueError("interval_seconds must be >= 1")
        self._session_factory = session_factory
        self._interval = int(interval_seconds)
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _job(self):
        try:
            deleted = delete_expired_urls(self._session_factory)
            if deleted:
                print(f"[UrlCleanupScheduler] deleted {deleted} expired url(s)")
        except Exception as exc:
            print(f"[UrlCleanupScheduler] cleanup error: {exc}")

    def _run_loop(self):
        while not self._stop_event.is_set():
            schedule.run_pending()
            # wait up to 1 second, return early if stop_event is set
            self._stop_event.wait(1)

    def start(self):
        """Start the scheduler (no-op if already running)."""
        if self._thread and self._thread.is_alive():
            return
        
        schedule.every(self._interval).seconds.do(self._job)

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="url-cleanup-scheduler")
        self._thread.start()

    def stop(self):
        """Stop the scheduler and wait briefly for the thread to finish."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None
