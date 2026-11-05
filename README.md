\# Infrastructure Monitoring \& Incident Response Lab



A virtual lab that monitors Linux servers, detects failures, raises alerts and automatically responds to incidents.



\## Architecture

| VM | Role | IP |

|----|------|----|

| monitor | Prometheus, Grafana, Alertmanager, Blackbox Exporter, Python responder | 192.168.56.10 |

| web01 | nginx web server + Node Exporter | 192.168.56.11 |

| app01 | PostgreSQL + Node Exporter | 192.168.56.12 |



Built on VirtualBox with Ubuntu Server 24.04 LTS (NAT + host-only networking).



\[Insert architecture diagram here: docs/architecture.png]



\## Stack

Prometheus - Node Exporter - Blackbox Exporter - Alertmanager - Grafana - Python - Bash - systemd - SSH key authentication



\## How it works

1\. Node Exporter exposes CPU, memory, disk, network and systemd service metrics.

2\. Prometheus scrapes every 15 seconds and evaluates 7 alert rules.

3\. Alertmanager sends firing and resolved alerts to a Python webhook responder.

4\. The responder logs each incident (JSON lines) and automatically restarts stopped services over SSH, using a sudoers rule that allows only that restart command.

5\. Grafana shows the live state of the environment.



\## Alert rules

InstanceDown, WebsiteDown, ServiceNotRunning, HighCPU, HighMemory, DiskSpaceLow, HighLatency (see prometheus/rules/alerts.yml).



\## Failure tests

| Failure | Method | Alert | Time to recover | Outcome |

|---------|--------|-------|-----------------|---------|

| nginx stopped | chaos.sh service | ServiceNotRunning, WebsiteDown | 35 s | Auto-restarted |

| Disk filled | chaos.sh disk | DiskSpaceLow | 95 s | Fixed manually (du, rm) |

| Network latency | chaos.sh network | HighLatency | 65 s | Self-cleared |

| VM powered off | VirtualBox | InstanceDown | 95 s | VM restarted |

| CPU stress | chaos.sh cpu | HighCPU | \[fill in] | \[fill in] |

| Memory stress | chaos.sh memory | HighMemory | \[fill in] | \[fill in] |

| Database stopped | chaos.sh db | ServiceNotRunning | \[fill in] | \[fill in] |



Times are from alert firing to resolved, in the incident log (UTC). See docs/sample-incidents.jsonl.



\## Screenshots

\[Add images from docs/screenshots/]



\## Runbooks and postmortems

\- runbooks/ - one runbook per alert

\- docs/postmortems/ - incident write-ups



\## What I learned

\[Write 4-5 sentences in your own words: Linux administration, networking, monitoring design, automation, troubleshooting.]



\## Future improvements

Telegram notifications, Ansible deployment, Loki log monitoring, firewall hardening, disk-cleanup automation.



\## Setup

Install order: VMs and networking, Node Exporter on targets, Prometheus + Alertmanager + Blackbox + Grafana on monitor, copy configs from this repo, enable the responder service.

