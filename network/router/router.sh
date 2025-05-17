#!/bin/bash

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

# Allow loopback (local) traffic
iptables -A INPUT -i lo -j ACCEPT

# Allow established/related packets (reply traffic)
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Block maliciuous IP
iptables -I INPUT 1 -s 198.51.100.23 -j DROP

# Allow http traffic
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Replace symbolic links with actual log files
rm -f /var/log/nginx/access.log /var/log/nginx/error.log
touch /var/log/nginx/access.log /var/log/nginx/error.log
chmod 666 /var/log/nginx/access.log /var/log/nginx/error.log

############################
# LOGGING
############################
iptables -A INPUT -j LOG --log-prefix "FW-INPUT: " --log-level 4
iptables -A OUTPUT -j LOG --log-prefix "FW-OUTPUT: " --log-level 4
rsyslogd

############################
# nginx
############################
/docker-entrypoint.sh nginx -g 'daemon off;'
