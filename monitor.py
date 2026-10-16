import requests
import json
from checker import check_service
import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("config.json not found. Please create it before running the monitor.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"config.json has a formatting error: {e}")
        raise


def local_secrets():
    try:
        with open("secrets.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("secrets.json not found. Please create it before running the monitor.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"secrets.json has a formatting error: {e}")
        raise


def send_alert(result, previous, webhook_url):
    current = result["status"]
    
    if current == "UP":
        emoji = "✓"
        headline = "RECOVERED"
    else:
        emoji = "!"
        headline = "PROBLEM"
    
    text = (
        f"{emoji} *{headline}*: {result['url']}\n"
        f"{previous} → {current} at {result['timestamp']}"
    )
    
    logging.info(f"Sending alert: {result['url']} {previous} → {current}")

    try:
        requests.post(webhook_url, json={"text": text}, timeout=5)
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Slack alert: {e}")

def main(last_status, urls, webhook_url):

    results = []

    for url in urls:
        result = check_service(url)
        results.append(result)
        
        message = f"{result['url']} is {result['status']} ({result['code']}) {result['response_time']}"
        
        if result["status"] == "UP": 
            logging.info(message)
        
        elif result["status"] == "WARNING":
            logging.warning(message)
        
        else:
            logging.error(message)
        
        previous = last_status.get(url)
        current = result["status"]
        
        if previous is not None and current != previous:
            send_alert(result, previous, webhook_url)
        
        last_status[url] = current

    with open("results.jsonl", "a") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    config = load_config()
    secrets = local_secrets()
    webhook_url = secrets["slack_webhook_url"]
    interval = config["interval_seconds"]
    last_status = {}
    
    try:
        while True:
            main(last_status, config["urls"], webhook_url)
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logging.info("Monitor stopped by the user.")