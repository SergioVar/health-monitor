import json
from checker import check_service
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


def main():
    
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

    with open("results.jsonl", "a") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(5)
    except KeyboardInterrupt:
        logging.info("Monitor stopped by the user.")