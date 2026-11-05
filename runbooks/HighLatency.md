# Runbook: HighLatency

**Severity:** warning

**What it means:** Website response time above 1 second.

## Diagnose
```
ping <host>; tc qdisc show; top; curl -w '%{time_total}\n' -o /dev/null -s <url>
```

## Fix
Remove network shaping, check server load, check the network path.

## Escalate
If not resolved in 15 minutes, check Grafana for related alerts and recent changes, then escalate to the system owner.
