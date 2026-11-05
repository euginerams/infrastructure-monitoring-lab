# Runbook: InstanceDown

**Severity:** critical

**What it means:** Node Exporter stopped answering. The host is down, rebooting or unreachable.

## Diagnose
```
ping <host>; check the VM state in VirtualBox; systemctl status prometheus-node-exporter
```

## Fix
Start the VM, or run: sudo systemctl restart prometheus-node-exporter

## Escalate
If not resolved in 15 minutes, check Grafana for related alerts and recent changes, then escalate to the system owner.
