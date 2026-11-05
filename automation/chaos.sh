#!/bin/bash
# Usage: ./chaos.sh <scenario>
case "$1" in
  service)       sudo systemctl stop nginx ;;                       # web01 only
  db)            sudo systemctl stop postgresql@16-main ;;          # app01 only
  cpu)           stress-ng --cpu 0 --timeout 180s ;;
  memory)        stress-ng --vm 1 --vm-bytes 650M --vm-keep --timeout 180s ;;
  disk)
    total=$(df --output=size -B1M / | tail -1 | tr -d ' ')
    avail=$(df --output=avail -B1M / | tail -1 | tr -d ' ')
    fill=$((avail - total / 10))
    sudo fallocate -l ${fill}M /fill.img
    echo "Disk now ~90% full. Run: ./chaos.sh disk-clean to fix" ;;
  disk-clean)    sudo rm -f /fill.img ;;
  network)
    sudo tc qdisc add dev enp0s8 root netem delay 1500ms
    echo "1.5s delay added for 120 seconds (SSH will feel slow)"
    (sleep 120 && sudo tc qdisc del dev enp0s8 root) &
    ;;
  *) echo "Usage: $0 {service|db|cpu|memory|disk|disk-clean|network}" ;;
esac
