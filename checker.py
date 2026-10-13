from datetime import datetime
import requests


def check_service(url):  #We defined a function
    
    timestamp = datetime.now().isoformat()
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            status = "UP"
        else:
            status = "WARNING"
        return {"url": url, "status": status, "code": response.status_code, "response_time": response.elapsed.total_seconds(), "timestamp": timestamp}
    
    except requests.exceptions.RequestException:
        return {"url": url, "status": "DOWN", "code": None, "response_time": None, "timestamp": timestamp}
        