# Network Diagnostic Automation Tool

## Overview

The Network Diagnostic Tool is a Python-based automation utility designed to troubleshoot network connectivity and service availability issues. It performs multiple health checks such as DNS resolution, ICMP ping, TCP connectivity, HTTP response validation, and SSL certificate inspection.

This tool helps engineers quickly identify whether a failure is related to DNS, network paths, open ports, or application response.

---

## Features

* DNS Resolution Check
* Ping Latency Measurement
* TCP Port Connectivity (80/443)
* HTTP Status Validation
* SSL Certificate Expiry Check
* Retry & Timeout Handling
* Parallel URL Processing
* JSON Report Generation

---

## Tech Stack

* Python 3
* Requests
* Socket
* SSL
* Subprocess
* Concurrent Futures

---

## Installation

```bash
pip3 install -r requirements.txt
```

---

## How to Run

```bash
python3 network_diagnostic.py --url https://google.com https://github.com
```

Optional arguments:

```
--timeout 5
--retry 3
```

---

## Output

* Console summary with status
* `report.json` containing detailed diagnostics

---

## Use Cases

* Production incident debugging
* API health validation
* Network troubleshooting
* DevOps monitoring

---

## Future Improvements

* Slack/Email alerting
* Continuous health monitoring
* Docker support
* Grafana integration

---
