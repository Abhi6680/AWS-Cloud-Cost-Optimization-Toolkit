"""Configuration, read from environment variables (never hardcode secrets)."""
import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class Config:
    dry_run: bool = True                  # SAFE DEFAULT: report only
    volume_min_age_days: int = 7          # ignore volumes younger than this
    snapshot_retention_days: int = 30     # snapshots older than this are candidates
    protect_tag_key: str = "DoNotDelete"  # resources with this tag=true are skipped


def load_config() -> Config:
    return Config(
        dry_run=_env_bool("DRY_RUN", True),
        volume_min_age_days=int(os.getenv("VOLUME_MIN_AGE_DAYS", "7")),
        snapshot_retention_days=int(os.getenv("SNAPSHOT_RETENTION_DAYS", "30")),
        protect_tag_key=os.getenv("PROTECT_TAG_KEY", "DoNotDelete"),
    )
