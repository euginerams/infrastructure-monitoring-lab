# Runbook: WebsiteDown

**Severity:** critical

**What it means:** The HTTP probe to the web server is failing.

## Diagnose
```
systemctl status nginx; journalctl -u nginx -n 30 --no-pager; ss -tulpn | grep :80
```

## Fix
sudo systemctl restart nginx (the responder does this automatically)

## Escalate
If not resolved in 15 minutes, check Grafana for related alerts and recent changes, then escalate to the system owner.
