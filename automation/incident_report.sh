#!/bin/bash
LOG=/var/log/incidents/incidents.jsonl
echo "=== Incident summary $(date) ==="
echo "Firing events:   $(grep -c '"status": "firing"' $LOG)"
echo "Resolved events: $(grep -c '"status": "resolved"' $LOG)"
echo "--- Last 15 events ---"
tail -n 15 $LOG | python3 -c "
import sys, json
for l in sys.stdin:
    e = json.loads(l)
    print(e['logged_at'], e['status'].upper(), e['alertname'], e['instance'], e.get('action',''), e.get('action_success',''))"
