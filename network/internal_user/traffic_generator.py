import socket
import requests
import time
import random
from scapy.all import IP, ICMP, send

def get_container_ip():
    """Get the IP address of the container."""
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def generate_icmp_traffic(source_ip, target_ip):
    """Send ICMP (ping) packets to the target IP."""
    print(f"Sending ICMP traffic from {source_ip} to {target_ip}")
    packet = IP(src=source_ip, dst=target_ip) / ICMP()
    send(packet, verbose=False)

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

def generate_dns_traffic(source_ip, dns_server, domain):
    """Send DNS queries to the DNS server."""
    print(f"Sending DNS traffic from {source_ip} to {dns_server} for domain {domain}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + \
                b'\x07' + domain.split('.')[0].encode() + b'\x03' + domain.split('.')[1].encode() + b'\x00\x00\x01\x00\x01'
        sock.sendto(query, (dns_server, 53))
        response, _ = sock.recvfrom(512)
        print(f"DNS Response: {response}")
    except Exception as e:
        print(f"DNS Query failed: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    # Get the container's IP address
    container_ip = get_container_ip()
    print(f"Container IP: {container_ip}")

    # Define targets
    webserver_ips = ["172.28.0.3"]  # Multiple webservers
    dns_server_ip = "172.28.0.21"  # DNS server
    external_ips = ["172.30.0.4", "172.30.0.5", "172.30.0.6"]  # External users
    domains = ["example.com", "test.com", "mywebsite.org"]  # Multiple domains

    # Run traffic generation for 2 minutes
    start_time = time.time()
    duration = 300  # 2 minutes in seconds

    while time.time() - start_time < duration:
        # Randomly select a target webserver and domain
        webserver_ip = random.choice(webserver_ips)
        domain = random.choice(domains)

        # Generate traffic to the webserver
        generate_http_traffic(container_ip, f"http://{webserver_ip}")

        # Generate traffic to the DNS server
        generate_dns_traffic(container_ip, dns_server_ip, domain)

        # Generate ICMP traffic to external IPs
        for external_ip in external_ips:
            if random.random() < 0.5:  # 50% chance to send ICMP traffic
                generate_icmp_traffic(container_ip, external_ip)

        # Random delay between 0.5 and 2 seconds
        time.sleep(random.uniform(0.5, 2))
