import sys

sys.path.insert(0, "src")
from ebs_cleanup.cleaner import estimate_monthly_cost  # noqa: E402
from ebs_cleanup.config import Config  # noqa: E402

CFG = Config()


def test_volume_cost():
    assert estimate_monthly_cost({"type": "volume", "size_gb": 100}, CFG) == 8.0


def test_snapshot_cost():
    assert estimate_monthly_cost({"type": "snapshot", "size_gb": 100}, CFG) == 5.0
