import psutil

def get_mac_address():
    for addresses in psutil.net_if_addrs().values():
        for address in addresses:
            if address.family == psutil.AF_LINK:
                return address.address
    return 'Could not retrieve MAC address'
