# Runbook: HighMemory

**Severity:** warning

**What it means:** Memory usage above 85% for 1 minute.

## Diagnose
```
free -h; ps aux --sort=-%mem | head
```

## Fix
Stop or restart the offending process; check for memory leaks.

## Escalate
If not resolved in 15 minutes, check Grafana for related alerts and recent changes, then escalate to the system owner.
