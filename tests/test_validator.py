import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, "src")
from ebs_cleanup.config import Config  # noqa: E402
from ebs_cleanup.validator import validate_snapshot, validate_volume  # noqa: E402

CFG = Config()
now = datetime.now(timezone.utc)


def test_old_volume_is_safe():
    vol = {"CreateTime": now - timedelta(days=30), "Tags": []}
    assert validate_volume(vol, CFG)[0] is True


def test_new_volume_is_skipped():
    vol = {"CreateTime": now - timedelta(days=1)}
    assert validate_volume(vol, CFG)[0] is False


def test_protected_volume_is_skipped():
    vol = {"CreateTime": now - timedelta(days=90),
           "Tags": [{"Key": "DoNotDelete", "Value": "true"}]}
    assert validate_volume(vol, CFG)[0] is False


def test_ami_snapshot_is_skipped():
    snap = {"SnapshotId": "snap-1", "StartTime": now - timedelta(days=90)}
    assert validate_snapshot(snap, CFG, {"snap-1"})[0] is False


def test_old_snapshot_is_safe():
    snap = {"SnapshotId": "snap-2", "StartTime": now - timedelta(days=90)}
    assert validate_snapshot(snap, CFG, set())[0] is True


def test_protected_snapshot_is_skipped():
    snap = {
        "SnapshotId": "snap-protected",
        "StartTime": now - timedelta(days=120),
        "Tags": [{"Key": "DoNotDelete", "Value": "true"}],
    }
    assert validate_snapshot(snap, CFG, set())[0] is False
