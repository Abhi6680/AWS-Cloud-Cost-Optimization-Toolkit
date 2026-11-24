"""Turns the report dict into plain text (later used as the SNS email body)."""


def format_report(report: dict) -> str:
    lines = [
        f"EBS Cleanup Report [{report['mode']}]",
        "=" * 44,
        f"Examined:            {report['total_examined']}",
        f"Safe to delete:      {report['deletable']} ({report['deletable_size_gb']} GB)",
        f"Orphaned snapshots:  {report['orphaned_snapshots']}",
        f"Deleted:             {report['deleted']}",
        f"Est. monthly saving: ${report['est_monthly_savings_usd']:.2f}",
        "",
    ]
    candidates = [i for i in report["items"] if i["safe"]]
    if candidates:
        lines.append("Candidates:")
        for i in candidates:
            lines.append(f"  - {i['type']:<8} {i['id']}  {i['size_gb']} GB  "
                         f"${i['est_monthly_cost_usd']:.2f}/mo  -> {i['action']}")
    else:
        lines.append("No cleanup candidates found.")
    skipped = report["total_examined"] - report["deletable"]
    lines.append(f"\nSkipped by validation: {skipped}")
    return "\n".join(lines)
