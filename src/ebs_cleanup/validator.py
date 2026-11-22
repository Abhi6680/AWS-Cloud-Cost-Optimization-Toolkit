"""Validation: decides whether a candidate is safe to delete.
Every function returns (is_safe, reason) so decisions are explainable in logs."""
from datetime import datetime, timezone

from .config import Config


def _age_days(timestamp: datetime) -> int:
    return (datetime.now(timezone.utc) - timestamp).days


def _is_protected(tags: list[dict] | None, protect_key: str) -> bool:
    for tag in tags or []:
        if tag["Key"] == protect_key and tag["Value"].lower() == "true":
            return True
    return False


def validate_volume(volume: dict, config: Config) -> tuple[bool, str]:
    if _is_protected(volume.get("Tags"), config.protect_tag_key):
        return False, f"protected by tag {config.protect_tag_key}=true"
    age = _age_days(volume["CreateTime"])
    if age < config.volume_min_age_days:
        return False, f"too new ({age}d < {config.volume_min_age_days}d)"
    return True, f"unattached and {age}d old"


def validate_snapshot(
    snapshot: dict, config: Config, ami_snapshot_ids: set[str]
) -> tuple[bool, str]:
    if _is_protected(snapshot.get("Tags"), config.protect_tag_key):
        return False, f"protected by tag {config.protect_tag_key}=true"
    if snapshot["SnapshotId"] in ami_snapshot_ids:
        return False, "used by an AMI"
    age = _age_days(snapshot["StartTime"])
    if age < config.snapshot_retention_days:
        return False, f"within retention ({age}d < {config.snapshot_retention_days}d)"
    return True, f"{age}d old, beyond retention"
