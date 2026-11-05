# Runbook: ServiceNotRunning

**Severity:** critical

**What it means:** A monitored systemd service is stopped.

## Diagnose
```
systemctl status <service>; journalctl -u <service> -n 30 --no-pager
```

## Fix
sudo systemctl restart <service> (automated by the responder). Investigate why it stopped.

## Escalate
If not resolved in 15 minutes, check Grafana for related alerts and recent changes, then escalate to the system owner.
