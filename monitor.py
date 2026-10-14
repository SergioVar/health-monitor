
import json
from checker import check_service
import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

def send_alert(result, previous):
    print("=" * 40)
    print(f"! STATE CHANGE: {result['url']}")
    print(f"   {previous} → {result['status']}")
    print(f"   at {result['timestamp']}")
    print("=" * 40)


def main(last_status):
    #List of services to monitor
    urls = [
        "https://www.google.com",
        "https://www.google.com/thispagedoesnotexist",
        "https://thisisnotarealwebsite12345.com",
    ]

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
            send_alert(result, previous)
        
        last_status[url] = current

    with open("results.jsonl", "a") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    last_status = {}
    try:
        while True:
            main(last_status)
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Monitor stopped by the user.")