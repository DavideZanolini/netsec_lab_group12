FROM python:3.11-slim

RUN apt update && apt install -y iproute2 && \
    pip3 install --break-system-packages scapy

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR /opt
COPY attack.py .

ENTRYPOINT ["/entrypoint.sh"]
