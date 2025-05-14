# netsec_lab_group12

how to generate traffic: build the containers, after 60 s the containers will start generating traffic

how to capture traffic:

- find the interfaces of the two networks: ip link
- open two terminals
- in each terminal run: sudo tcpdump -i <right interface> -w <file name>
- merge the two files to obtain a single final file: mergecap -w combined.pcap eth0.pcap eth1.pcap

## Attack

### DDoS

`ddos` service in docker-compose.yml

Capture the traffic on the router with

```bash
docker exec -it router tcpdump -n -i any dst 172.30.0.2 and udp
```
