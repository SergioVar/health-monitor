# Health Monitor

A service monitor that periodically checks websites, records their status (UP / WARNING / DOWN), saves a history, and sends alerts to Slack when a service changes state.

## Requirements

- Python 3.10+
- The libraries from `requirements.txt`

## Installation

```bash
# Create and activate the virtual environment
python -m venv venv
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt