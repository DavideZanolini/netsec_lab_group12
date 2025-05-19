from scapy.all import sniff, IP, TCP, UDP, ICMP, Ether
import time
import os

LOG_DIR = "/tmp/router_logs"
LOG_FILE = os.path.join(LOG_DIR, "iptables.log")
INTERFACES = ["eth0", "eth1"]

os.makedirs(LOG_DIR, exist_ok=True)

def log_packet(pkt):
    iso_timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
    micro = f"{int(time.time() * 1_000_000) % 1_000_000:06d}"
    iso_timestamp = f"{iso_timestamp}.{micro}+00:00"

    boot_time = int(time.time()) % 20000 + 10000
    boot_micro = f"{random.randint(100000,999999)}"
    boot_str = f"{boot_time}.{boot_micro}"

    prefix = "FW:"
    mac = pkt[Ether].src if Ether in pkt else "-"
    src = pkt[IP].src if IP in pkt else "-"
    dst = pkt[IP].dst if IP in pkt else "-"
    proto = "-"
    spt = "-"
    dpt = "-"
    if TCP in pkt:
        proto = "TCP"
        spt = pkt[TCP].sport
        dpt = pkt[TCP].dport
    elif UDP in pkt:
        proto = "UDP"
        spt = pkt[UDP].sport
        dpt = pkt[UDP].dport
    elif ICMP in pkt:
        proto = "ICMP"
    length = len(pkt)
    iface = pkt.sniffed_on if hasattr(pkt, "sniffed_on") else "-"

    log_line = (f"{iso_timestamp} router kernel: [{boot_str}] {prefix} IN={iface} OUT= "
                f"MAC={mac} SRC={src} DST={dst} PROTO={proto} "
                f"SPT={spt} DPT={dpt} LEN={length}\n")
    with open(LOG_FILE, "a") as f:
        f.write(log_line)

def main():
    sniff(prn=log_packet, store=0, iface=INTERFACES)

if __name__ == "__main__":
    import random
    main()