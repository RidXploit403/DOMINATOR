
# Dominator V.1 -  DoS Tool

Dominator is a simple DoS (Denial of Service) tool written in Python. It allows users to perform HTTP GET and POST requests to a specified target site, simulating a flood of requests to test the site's resilience.

## Features

- Supports both GET and POST requests.
- Customizable user-agent headers.
- Option to add custom headers to requests.
- Safe mode to automatically shut down after the attack.
- Multi-threaded for increased performance.

## Requirements

- Python 3.x
- `requests` library (install via `pip install requests`)

## Usage

To run the tool, use the following command:

```bash
pkg install python
pkg install git
pip install requests
git clone https://github.com/RidXploit403/DOMINATOR.git
cd DOMINATOR
python DDoSV1.py
