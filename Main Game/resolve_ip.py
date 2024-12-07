from scapy.all import ARP, Ether, srp, conf, get_if_addr

def get_local_mac():
    # Sends an ARP request to retrieve the MAC address of the local machine
    # Automatically get the active network interface
    active_interface = conf.iface  # Scapy will select the default active interface
    
    # Get the local IP address of the active interface
    local_ip = get_if_addr(active_interface)
    
    # Create an ARP request packet for the local IP
    arp_request = ARP(pdst=local_ip)
    
    # Create an Ethernet frame to broadcast the ARP request
    ether_request = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
    
    # Combine Ethernet frame and ARP request
    packet = ether_request / arp_request
    
    # Send the packet and capture the response
    result = srp(packet, timeout=1, verbose=False)[0]
    
    # Extract the MAC address from the response
    if result:
        return result[0][1].hwsrc
    else:
        return None

def main():
    mac_address = get_local_mac()
    if mac_address:
        print(f"The MAC address of your system is: {mac_address}")
    else:
        print("Unable to retrieve the MAC address.")

if __name__ == "__main__":
    main()
