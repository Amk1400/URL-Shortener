from dataclasses import dataclass
import os


@dataclass
class AppConfig:
    """Application configuration dataclass.

    Attributes:
        ttl_minutes (int): time-to-live in minutes for short urls.
        database_url (str): SQLAlchemy database URL.
    """
    ttl_minutes: int
    database_url: str

    @classmethod
    def load(cls) -> "AppConfig":
        """
        Load config from environment variables.

        Args:
            None

        Returns:
            AppConfig: Loaded configuration.

        Raises:
            ValueError: If TTL is not a valid integer.
        """
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "secret")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "url_db")

        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        return cls(
            ttl_minutes=int(os.getenv("APP_TTL_MINUTES", "24")),
            database_url=os.getenv("DATABASE_URL", database_url),
        )
