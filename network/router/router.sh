#!/bin/bash

python3 /logs_generator.py &

# ROUTER
# Enable IP forwarding
echo 1 >/proc/sys/net/ipv4/ip_forward

############################
# NAT
############################
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth1 -j ACCEPT
iptables -A FORWARD -i eth0 -j ACCEPT

############################
# FIREWALL
############################
# Set default policies
iptables -P INPUT DROP    # drop all incoming unless explicitly allowed
iptables -P FORWARD DROP  # drop all forwarded unless explicitly allowed
iptables -P OUTPUT ACCEPT # allow all outgoing

# Log and allow loopback (local) traffic
iptables -A INPUT -i lo -j LOG --log-prefix "FW-LOOPBACK: " --log-level 4
iptables -A INPUT -i lo -j ACCEPT

# Log and allow established/related packets (reply traffic)
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j LOG --log-prefix "FW-ESTABLISHED: " --log-level 4
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Log and block malicious IP
iptables -I INPUT 1 -s 198.51.100.23 -j LOG --log-prefix "FW-BLOCKED: " --log-level 4
iptables -I INPUT 2 -s 198.51.100.23 -j DROP

# Log and allow http traffic
iptables -A INPUT -p tcp --dport 80 -j LOG --log-prefix "FW-HTTP: " --log-level 4
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Log all other dropped packets
iptables -A INPUT -j LOG --log-prefix "FW-DROP: " --log-level 4

# Replace symbolic links with actual log files
rm -f /var/log/nginx/access.log /var/log/nginx/error.log
touch /var/log/nginx/access.log /var/log/nginx/error.log
chmod 666 /var/log/nginx/access.log /var/log/nginx/error.log

rsyslogd

############################
# nginx
############################
/docker-entrypoint.sh nginx -g 'daemon off;'