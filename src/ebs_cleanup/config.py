"""Configuration, read from environment variables (never hardcode secrets)."""
import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in ("1", "true", "yes", "on"):
        return True
    if normalized in ("0", "false", "no", "off"):
        return False
    raise ValueError(
        f"Invalid value for {name}: {value!r}. Use true/false, yes/no, or 1/0."
    )


def _positive_int(name: str, default: int) -> int:
    raw_value = os.getenv(name, str(default))
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be a whole number; got {raw_value!r}.") from exc
    if value < 0:
        raise ValueError(f"{name} cannot be negative.")
    return value


@dataclass(frozen=True)
class Config:
    dry_run: bool = True                  # SAFE DEFAULT: report only
    volume_min_age_days: int = 7          # ignore volumes younger than this
    snapshot_retention_days: int = 30     # snapshots older than this are candidates
    protect_tag_key: str = "DoNotDelete"  # resources with this tag=true are skipped


def load_config() -> Config:
    return Config(
        dry_run=_env_bool("DRY_RUN", True),
        volume_min_age_days=_positive_int("VOLUME_MIN_AGE_DAYS", 7),
        snapshot_retention_days=_positive_int("SNAPSHOT_RETENTION_DAYS", 30),
        protect_tag_key=os.getenv("PROTECT_TAG_KEY", "DoNotDelete"),
    )
