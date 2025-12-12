import threading
import time
from typing import Callable, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.orm import URL

def delete_expired_urls(session_factory: Callable[[], Session]) -> int:
    """
    Delete all URL rows where expired_at is set and expired_at < now().
    Returns number of rows deleted.
    """
    session: Session = session_factory()
    try:
        # select rows that have expired (expired_at not null and less than now)
        q = session.query(URL).filter(URL.expired_at != None, URL.expired_at < func.now())
        count = q.count()
        if count > 0:
            # perform bulk delete
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
    Simple background scheduler that runs delete_expired_urls every `interval_seconds`.
    The scheduler runs in a daemon thread so it won't block process shutdown.
    """

    def __init__(self, session_factory: Callable[[], Session], interval_seconds: int = 60):
        """
        :param session_factory: callable that returns a new SQLAlchemy Session (e.g. DatabaseSession.get_session)
        :param interval_seconds: how often to run cleanup (in seconds). Default: 60 (1 minute).
        """
        self._session_factory = session_factory
        self._interval = interval_seconds
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def _loop(self):
        # run at start, then sleep interval
        while not self._stop_event.is_set():
            try:
                deleted = delete_expired_urls(self._session_factory)
                # optional: print/logging here; keep minimal to avoid silent failures
                if deleted:
                    print(f"[UrlCleanupScheduler] deleted {deleted} expired url(s)")
            except Exception as exc:
                # swallow exceptions but print so they can be observed in logs
                print(f"[UrlCleanupScheduler] cleanup error: {exc}")
            # sleep but react quickly to stop event
            finished = self._stop_event.wait(self._interval)
            if finished:
                break

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True, name="url-cleanup-scheduler")
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
            self._thread = None
