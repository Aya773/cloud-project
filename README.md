# Cloud Architecture Project: Container vs. App on a VM

Compares an app running directly on an Ubuntu VM with the same app
in a Docker container inside that VM (startup time, memory, throughput),
plus the time to boot a new VM.

## Environment
- MacBook Pro, Apple M2, 8 GB RAM
- Multipass 1.17.0 (QEMU driver), Ubuntu 26.04.1 LTS (aarch64), 1 vCPU, 2 GB RAM
- Docker 29.1.3 (Ubuntu docker.io package), image python:3.14-slim
- Load tool: ApacheBench (20,000 requests, 10 concurrent)

## Files
- app.py: the test web server (returns "hello")
- Dockerfile: builds the container image
- measure.sh: runs 3 measurement runs per setup, writes results.csv
- results_threaded.csv: final dataset (threaded server)
- results_run1_singlethread.csv: first run, kept as a record
- boot_times.txt: three VM boot-time runs
- make_charts.py: produces the chart_*.png files
- architecture.drawio.png: architecture diagram (can be reopened and edited in draw.io)

## How to reproduce
1. Launch an Ubuntu VM with Multipass and install docker.io and apache2-utils.
2. Copy app.py, Dockerfile and measure.sh into the VM.
3. Run: docker build -t hello-app . && ./measure.sh
4. Run make_charts.py on the results (needs pandas and matplotlib).

No secrets or personal data are included.
