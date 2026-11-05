# Runbook: DiskSpaceLow

**Severity:** critical

**What it means:** Less than 20% disk space free.

## Diagnose
```
df -h; sudo du -sh /* 2>/dev/null | sort -h | tail
```

## Fix
Delete unneeded large files, rotate logs (journalctl --vacuum-size=100M), or expand the disk.

## Escalate
If not resolved in 15 minutes, check Grafana for related alerts and recent changes, then escalate to the system owner.
