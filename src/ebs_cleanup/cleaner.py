"""Orchestrator: discover -> validate -> (dry-run report | delete)."""
import logging

from botocore.exceptions import ClientError

from .config import Config
from .discovery import find_own_snapshots, find_unattached_volumes, get_ami_snapshot_ids
from .validator import validate_snapshot, validate_volume

logger = logging.getLogger(__name__)


def _delete(ec2, kind: str, resource_id: str) -> str:
    """Returns 'deleted' or 'failed: <reason>'."""
    try:
        if kind == "volume":
            ec2.delete_volume(VolumeId=resource_id)
        else:
            ec2.delete_snapshot(SnapshotId=resource_id)
        return "deleted"
    except ClientError as err:
        code = err.response["Error"]["Code"]
        logger.error("Failed to delete %s %s: %s", kind, resource_id, code)
        return f"failed: {code}"


def estimate_monthly_cost(item: dict, config: Config) -> float:
    """Estimated USD/month for one item. Upper bound for snapshots, because
    snapshots are incremental and may store less than their full volume size."""
    price = config.volume_price_per_gb if item["type"] == "volume" \
        else config.snapshot_price_per_gb
    return round(item["size_gb"] * price, 2)


def run_cleanup(ec2, config: Config) -> dict:
    mode = "DRY-RUN" if config.dry_run else "LIVE"
    logger.info("Starting EBS cleanup in %s mode", mode)

    items = []  # one entry per candidate, with the decision and outcome

    for vol in find_unattached_volumes(ec2):
        safe, reason = validate_volume(vol, config)
        items.append({"type": "volume", "id": vol["VolumeId"],
                      "size_gb": vol["Size"], "safe": safe, "reason": reason})

    ami_ids = get_ami_snapshot_ids(ec2)
    for snap in find_own_snapshots(ec2):
        safe, reason = validate_snapshot(snap, config, ami_ids)
        items.append({"type": "snapshot", "id": snap["SnapshotId"],
                      "size_gb": snap["VolumeSize"], "safe": safe, "reason": reason})

    for item in items:
        item["est_monthly_cost_usd"] = estimate_monthly_cost(item, config)
        if not item["safe"]:
            item["action"] = "skipped"
        elif config.dry_run:
            item["action"] = "would delete (dry-run)"
        else:
            item["action"] = _delete(ec2, item["type"], item["id"])
        logger.info("%s %s -> %s (%s)", item["type"], item["id"],
                    item["action"], item["reason"])

    deletable = [i for i in items if i["safe"]]
    report = {
        "mode": mode,
        "total_examined": len(items),
        "deletable": len(deletable),
        "deletable_size_gb": sum(i["size_gb"] for i in deletable),
        "deleted": sum(1 for i in items if i["action"] == "deleted"),
        "est_monthly_savings_usd": round(
            sum(i["est_monthly_cost_usd"] for i in deletable), 2),
        "items": items,
    }
    logger.info("Summary: %s", {k: v for k, v in report.items() if k != "items"})
    return report
