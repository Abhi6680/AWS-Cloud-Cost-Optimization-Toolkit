import sys

sys.path.insert(0, "src")
from ebs_cleanup.discovery import is_orphaned_snapshot  # noqa: E402
from ebs_cleanup.report import format_report  # noqa: E402


def test_orphaned_when_volume_gone():
    assert is_orphaned_snapshot({"VolumeId": "vol-old"}, {"vol-new"}) is True


def test_not_orphaned_when_volume_exists():
    assert is_orphaned_snapshot({"VolumeId": "vol-1"}, {"vol-1"}) is False


def test_copied_snapshot_not_flagged():
    assert is_orphaned_snapshot({"VolumeId": "vol-ffffffff"}, set()) is False


def test_report_text_contains_key_fields():
    report = {"mode": "DRY-RUN", "total_examined": 1, "deletable": 1,
              "deletable_size_gb": 10, "orphaned_snapshots": 0, "deleted": 0,
              "est_monthly_savings_usd": 0.8,
              "items": [{"type": "volume", "id": "vol-1", "size_gb": 10, "safe": True,
                         "est_monthly_cost_usd": 0.8, "action": "would delete (dry-run)"}]}
    text = format_report(report)
    assert "DRY-RUN" in text and "vol-1" in text and "$0.80" in text
