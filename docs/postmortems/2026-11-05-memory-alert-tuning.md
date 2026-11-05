# Postmortem: HighMemory alert did not fire during memory stress tests

**Date:** 2026-11-05 (times in UTC; Cape Town is UTC+2)
**Severity:** Low (monitoring gap found during testing)
**Type:** Deliberate failure injection (`chaos.sh memory`)

## Summary
The first memory stress tests did not trigger the `HighMemory` alert. Troubleshooting showed two causes: the alert rule on the monitor still had its original 85% threshold after I thought I had lowered it, and the test load was too small for a VM with 4 GB of RAM. After correcting both, the alert fired as designed.

## Timeline and measurements (web01, 4 GB RAM, baseline memory use about 11.7%)
| Test load | Peak memory use | Result |
|-----------|-----------------|--------|
| 650 MB (fixed size) | about 28% | No alert (below threshold) |
| 65% of RAM | 67.1% | No alert (below the 70% threshold) |
| 80% of RAM | 80.5% (brief peak 89.2%) | `HighMemory` fired at 14:23:33 UTC |

## Root cause
- The rule file on the monitor still contained `> 85` because my first edit had not been applied. I found this by reading the file with `grep` and checking the loaded rule through the Prometheus API.
- The test loads were sized for a smaller VM. Measuring web01's memory live with a query loop showed the real numbers.

## What worked
- Prometheus kept scraping web01 under load, and the rule fired once usage stayed above 70% for the `for: 1m` period
- The incident responder logged the alert automatically

## Lessons and improvements
- Verify the loaded configuration, not just the file you edited (`promtool check rules` and the Prometheus rules API)
- Size stress tests as a percentage of RAM so they scale with the VM
- Measure the metric during the test instead of assuming the load was enough
- An earlier test at 90% of RAM coincided with a brief `InstanceDown` on web01, a reminder that near-total memory exhaustion can make a host stop answering scrapes, so keep a host-level alert alongside threshold alerts
