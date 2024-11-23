import socket
import requests
import psutil

def get_ip_addresses():
    private_ip = socket.gethostbyname(socket.gethostname())
    public_ip = None
    ipv6_address = None
    try:
        public_ip = requests.get('https://api.ipify.org').text
    except requests.RequestException:
        public_ip = 'Could not retrieve public IP'
    
    try:
        ipv6_address = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][0]
    except Exception:
        ipv6_address = 'Could not retrieve IPv6'

    return private_ip, public_ip, ipv6_address

def get_network_info():
    network_info = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # Corrected here
                network_info.append(f"{interface}: {addr.address}")
    return '\n'.join(network_info)
