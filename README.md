# netsec_lab_group12

how to generate traffic: build the containers, after 60 s the containers will start generating traffic

how to capture traffic:

- find the interfaces of the two networks: ip link
- open two terminals
- in each terminal run: sudo tcpdump -i <right interface> -w <file name>
- merge the two files to obtain a single final file: mergecap -w combined.pcap eth0.pcap eth1.pcap

## Attacks

### Port Scan

```bash
docker exec -it attacker bash
nmap 172.30.0.2
```

### DDoS

```bash
docker exec -it attacker bash
python3 /opt/ddos.py
```

Capture the traffic on the router with

```bash
docker exec -it router tcpdump -n -i any dst 172.30.0.2 and udp
```
