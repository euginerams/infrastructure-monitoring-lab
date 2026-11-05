# Runbook: HighCPU

**Severity:** warning

**What it means:** CPU usage above 80% for 1 minute.

## Diagnose
```
top -o %CPU; ps aux --sort=-%cpu | head
```

## Fix
Identify and stop the runaway process, or scale resources.

## Escalate
If not resolved in 15 minutes, check Grafana for related alerts and recent changes, then escalate to the system owner.
