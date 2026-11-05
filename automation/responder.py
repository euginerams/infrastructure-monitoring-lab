#!/usr/bin/env python3
"""Receives Alertmanager webhooks, logs incidents, auto-restarts stopped services."""
import json, subprocess, datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

LOG = "/var/log/incidents/incidents.jsonl"
SSH_KEY = "/home/labadmin/.ssh/lab_key"
SSH_USER = "labadmin"
SERVICES = {"nginx.service": "nginx", "postgresql@16-main.service": "postgresql"}

def log(event):
    event["logged_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    with open(LOG, "a") as f:
        f.write(json.dumps(event) + "\n")

def restart(host, service):
    cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no",
           f"{SSH_USER}@{host}", f"sudo systemctl restart {service}"]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30).returncode == 0
    except Exception:
        return False

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        for a in data.get("alerts", []):
            labels = a["labels"]
            event = {
                "status": a["status"],
                "alertname": labels.get("alertname"),
                "instance": labels.get("instance"),
                "severity": labels.get("severity"),
                "summary": a["annotations"].get("summary"),
                "startsAt": a["startsAt"],
            }
            if a["status"] == "firing" and labels.get("alertname") == "ServiceNotRunning":
                host = labels["instance"].split(":")[0]
                svc = SERVICES.get(labels.get("name"))
                if svc:
                    event["action"] = f"restart {svc} on {host}"
                    event["action_success"] = restart(host, svc)
            log(event)
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass

HTTPServer(("0.0.0.0", 5001), Handler).serve_forever()
