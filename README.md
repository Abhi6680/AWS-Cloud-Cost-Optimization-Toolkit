# AWS Cloud Cost Optimization Toolkit – Automated EBS Resource Cleanup

Serverless Python tool that finds unattached EBS volumes and old snapshots,
validates them, and deletes them only when dry-run is explicitly disabled.

## Quick start

Create and activate a virtual environment:

```bash
python -m venv venv
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Install dependencies and run the tests:

```bash
pip install -r requirements.txt pytest
pytest tests/                   # unit tests, no AWS needed
```

Configure an AWS profile and run the toolkit in its default dry-run mode:

```bash
aws configure --profile ebs-toolkit
python run_local.py --profile ebs-toolkit --region <your-region>
```

## Safety

The toolkit should be run in dry-run mode first. Review the cleanup report and
verify that each candidate is safe to remove before enabling any deletion.
Never commit AWS credentials, access keys, or secret configuration files.

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
