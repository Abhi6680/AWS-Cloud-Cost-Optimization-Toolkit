# AWS Cloud Cost Optimization Toolkit – Automated EBS Resource Cleanup

Serverless Python tool that finds unattached EBS volumes and old snapshots,
validates them, and deletes them only when dry-run is explicitly disabled.

## Quick start
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt pytest
pytest tests/                   # unit tests, no AWS needed
aws configure --profile ebs-toolkit
python run_local.py --profile ebs-toolkit --region <your-region>   # DRY-RUN
```

## Configuration (environment variables)
| Variable | Default | Meaning |
|---|---|---|
| DRY_RUN | true | Set `false` to really delete |
| VOLUME_MIN_AGE_DAYS | 7 | Skip volumes newer than this |
| SNAPSHOT_RETENTION_DAYS | 30 | Snapshots older than this are candidates |
| PROTECT_TAG_KEY | DoNotDelete | Tag `<key>=true` protects a resource |
| VOLUME_PRICE_PER_GB | 0.08 | Estimate price, USD per GB-month |
| SNAPSHOT_PRICE_PER_GB | 0.05 | Estimate price, USD per GB-month |

## Roadmap
- [x] Discovery, validation, dry-run, Lambda handler
- [x] Estimated monthly cost in report
- [ ] Least-privilege IAM policy
- [ ] Deploy to Lambda
- [ ] EventBridge schedule
- [ ] SNS email report + CloudWatch alarm
- [ ] Architecture diagram, demo
