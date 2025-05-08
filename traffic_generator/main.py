import socket
import requests
import time
from scapy.all import IP, ICMP, send

def generate_icmp_traffic(source_ip, target_ip):
    """Send ICMP (ping) packets to the target IP."""
    print(f"Sending ICMP traffic from {source_ip} to {target_ip}")
    packet = IP(src=source_ip, dst=target_ip)/ICMP()
    send(packet, verbose=False)

def generate_http_traffic(source_ip, target_url):
    """Send HTTP GET requests to the target URL."""
    print(f"Sending HTTP traffic from {source_ip} to {target_url}")
    try:
        response = requests.get(target_url, headers={"X-Forwarded-For": source_ip})
        print(f"HTTP Response Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")

def generate_dns_traffic(source_ip, dns_server, domain):
    """Send DNS queries to the DNS server."""
    print(f"Sending DNS traffic from {source_ip} to {dns_server} for domain {domain}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query = b'\xaa\xaa\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + \
                b'\x07example\x03com\x00\x00\x01\x00\x01'
        sock.sendto(query, (dns_server, 53))
        response, _ = sock.recvfrom(512)
        print(f"DNS Response: {response}")
    except Exception as e:
        print(f"DNS Query failed: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    # Define targets and sources
    icmp_targets = ["192.168.1.10", "192.168.1.11", "192.168.1.12"]  # Internal users
    http_target = "http://10.0.1.5"  # Webserver
    dns_server = "10.0.1.53"  # DNS server
    domain = "example.com"
    source_ips = ["10.0.1.2", "10.0.1.3", "10.0.1.4"]  # External users

    # Run traffic generation for 2 minutes
    start_time = time.time()
    duration = 120  # 2 minutes in seconds

    while time.time() - start_time < duration:
        for source_ip in source_ips:
            for target_ip in icmp_targets:
                generate_icmp_traffic(source_ip, target_ip)
            generate_http_traffic(source_ip, http_target)
            generate_dns_traffic(source_ip, dns_server, domain)
            time.sleep(1)  # Add a small delay to avoid overwhelming the network