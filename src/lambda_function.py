"""AWS Lambda entry point. Handler setting: lambda_function.lambda_handler"""
import logging

import boto3

from ebs_cleanup.cleaner import run_cleanup
from ebs_cleanup.config import load_config

logging.getLogger().setLevel(logging.INFO)  # Lambda pre-configures the root logger


def lambda_handler(event, context):
    config = load_config()
    ec2 = boto3.client("ec2")  # region + credentials come from the Lambda role
    report = run_cleanup(ec2, config)
    return {k: v for k, v in report.items() if k != "items"}
