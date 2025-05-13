import socket
import requests
import time
import random

def get_container_ip():
    """Get the IP address of the container."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def generate_http_traffic(source_ip, target_url):
    """Send HTTP GET and POST requests to the target URL."""
    methods = ["GET", "POST"]
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "curl/7.68.0",
            "Python-requests/2.25.1"
        ]),
        "X-Forwarded-For": source_ip
    }
    method = random.choice(methods)
    print(f"Sending HTTP {method} traffic from {source_ip} to {target_url}")
    try:
        if method == "GET":
            response = requests.get(target_url, headers=headers)
        elif method == "POST":
            response = requests.post(target_url, headers=headers, data={"key": "value"})
        print(f"HTTP {method} Response Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP {method} Request failed: {e}")

if __name__ == "__main__":
    # Get the container's IP address
    container_ip = get_container_ip()
    print(f"Container IP: {container_ip}")

    # Define the target webserver
    webserver_ip = "172.30.0.2"
    duration = 300  # Run traffic generation for 5 minutes

    time.sleep(30)

    # Start generating traffic
    start_time = time.time()
    while time.time() - start_time < duration:
        # Generate HTTP traffic
        generate_http_traffic(container_ip, f"http://{webserver_ip}")

        # Random delay between 0.5 and 2 seconds
        time.sleep(random.uniform(0.5, 2))