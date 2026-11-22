"""Run the toolkit from your laptop. Defaults to DRY-RUN.
Usage:  python run_local.py --profile myprofile --region ap-south-1"""
import argparse
import logging
import sys

import boto3

sys.path.insert(0, "src")
from ebs_cleanup.cleaner import run_cleanup  # noqa: E402
from ebs_cleanup.config import load_config  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

parser = argparse.ArgumentParser()
parser.add_argument("--profile", default=None)
parser.add_argument("--region", required=True)
args = parser.parse_args()

session = boto3.Session(profile_name=args.profile, region_name=args.region)
run_cleanup(session.client("ec2"), load_config())
