from dataclasses import dataclass
import os
from pathlib import Path


ENV_FILE = Path(__file__).resolve().parent / ".env"


def load_env_file(path: Path = ENV_FILE) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_env_file()


@dataclass(frozen=True)
class DatabaseConfig:
    host: str = os.getenv("AGRI_DB_HOST", "127.0.0.1")
    port: int = int(os.getenv("AGRI_DB_PORT", "3306"))
    user: str = os.getenv("AGRI_DB_USER", "root")
    password: str = os.getenv("AGRI_DB_PASSWORD", "")
    database: str = os.getenv("AGRI_DB_NAME", "agri_warning")
    charset: str = "utf8mb4"


DB_CONFIG = DatabaseConfig()
LOGIN_USER = os.getenv("AGRI_LOGIN_USER", "admin")
LOGIN_PASSWORD = os.getenv("AGRI_LOGIN_PASSWORD", "123456")
