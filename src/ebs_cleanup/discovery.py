"""Discovery: read-only calls that find candidate resources."""


def find_unattached_volumes(ec2) -> list[dict]:
    """Volumes in 'available' state are not attached to any instance."""
    volumes = []
    paginator = ec2.get_paginator("describe_volumes")
    for page in paginator.paginate(
        Filters=[{"Name": "status", "Values": ["available"]}]
    ):
        volumes.extend(page["Volumes"])
    return volumes


def find_own_snapshots(ec2) -> list[dict]:
    """Only snapshots owned by this account (not public/shared ones)."""
    snapshots = []
    paginator = ec2.get_paginator("describe_snapshots")
    for page in paginator.paginate(OwnerIds=["self"]):
        snapshots.extend(page["Snapshots"])
    return snapshots


def get_ami_snapshot_ids(ec2) -> set[str]:
    """Snapshot IDs used by our AMIs. These cannot be deleted while the AMI exists."""
    ids = set()
    for image in ec2.describe_images(Owners=["self"])["Images"]:
        for mapping in image.get("BlockDeviceMappings", []):
            snap_id = mapping.get("Ebs", {}).get("SnapshotId")
            if snap_id:
                ids.add(snap_id)
    return ids


def get_existing_volume_ids(ec2) -> set[str]:
    """IDs of all volumes that currently exist (attached or not)."""
    ids = set()
    paginator = ec2.get_paginator("describe_volumes")
    for page in paginator.paginate():
        ids.update(v["VolumeId"] for v in page["Volumes"])
    return ids


def is_orphaned_snapshot(snapshot: dict, existing_volume_ids: set[str]) -> bool:
    """True if the snapshot's source volume no longer exists.
    Copied snapshots report 'vol-ffffffff' (no real source), so we ignore those."""
    source = snapshot.get("VolumeId")
    if not source or source == "vol-ffffffff":
        return False
    return source not in existing_volume_ids
