# Postmortem: nginx stopped on web01

**Date:** 2026-11-04 (times in UTC; Cape Town is UTC+2)
**Severity:** Critical (simulated)
**Type:** Deliberate failure injection (`chaos.sh service`)

## Summary
The nginx service on web01 was stopped on purpose to test detection and automated remediation.

## Timeline (UTC)
- 20:47:58 - Prometheus fires `ServiceNotRunning` and `WebsiteDown`
- 20:48:23 - Alertmanager delivers the alerts to the responder; the responder restarts nginx over SSH (success)
- 20:48:33 - Both alerts resolve

## Impact
The website was unreachable until the automatic restart completed. Detection to recovery took about 35 seconds.

## Root cause
Service stopped manually as part of the test.

## What worked
- systemd collector in Node Exporter detected the stopped unit
- Blackbox probe independently confirmed the website was down
- Automated restart restored service with no human action

## Improvements
- Add a restart-loop limit so a crashing service is not restarted endlessly
- Add Telegram/email notification alongside auto-remediation
- Add a disk-cleanup action for DiskSpaceLow
