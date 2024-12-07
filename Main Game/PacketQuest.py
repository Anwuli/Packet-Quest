import pygame
import moviepy
import sys
from resolve_ip import get_local_mac
from scapy.all import IP, ICMP, ARP, conf, send, Ether, get_if_addr, Raw
from scapy.all import ARP, Ether, srp, conf, get_if_addr, sendp


# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Mac Murder Mystery')

# Load background images
background = pygame.image.load('startmenuimage3.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
bonus_background = pygame.image.load('creditsimage.png')
bonus_background = pygame.transform.scale(bonus_background, (screen_width, screen_height))
glossary_background = pygame.image.load('creditsimage.png')
glossary_background = pygame.transform.scale(glossary_background, (screen_width, screen_height))

# Define colors
TEXT_COLOR = (125, 57, 49)
BUTTON_COLOR = (210, 191, 148, 150)  # Semi-transparent color

# Set up the clock
clock = pygame.time.Clock()

# Set up fonts
pygame.font.init()
haunted_font = pygame.font.Font(None, 50)  # Use for title
vintage_rotter_font = pygame.font.Font(r'Fonts\vintage_rotter.otf', 40)  # Custom font
arial_font = pygame.font.Font(r'Fonts\arial_narrow.ttf', 25)
roboto_font = pygame.font.Font(r'Fonts\Roboto-Black.ttf', 50)

from scapy.all import sendp

def generate_arp_packet(dest_ip, num_packets, payload=None): 
    # Generate and send ARP packets using Scapy.
    # Get the default active interface and its IP address
    active_interface = conf.iface
    source_ip = get_if_addr(active_interface)
    packets = []

    for _ in range(num_packets):
        # Build ARP packet
        arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(psrc=source_ip, pdst=dest_ip)
        
        # Add payload if provided
        if payload:
            arp_packet = arp_packet / Raw(load=payload)
        
        packets.append(arp_packet)

    # Send the packets on the network
    sendp(packets, iface=active_interface, verbose=True)
    return packets

from scapy.all import Ether, IP, ICMP, Raw, send, sendp

# Call the function

from scapy.all import Ether, IP, Raw, sendp, get_if_addr, getmacbyip, conf

def generate_ip_packet(dest_ip, num_packets, payload=None):
    # Generate and send IP packets using Scapy.
    active_interface = conf.iface  # Scapy will select the default active interface
    source_ip = get_if_addr(active_interface)  # Get the source IP address of the active interface
    packets = []

    try:
        for _ in range(num_packets):
            # Build Ethernet + IP packet
            
            ip_packet = IP(src=source_ip, dst=dest_ip) / ICMP()

            # Add payload if provided
            if payload:
                ip_packet = ip_packet / Raw(load=payload)

            packets.append(ip_packet)
            send(ip_packet, count=num_packets)

    except Exception as e:
        print(f"Error occurred while generating packets: {e}")

    return packets


from scapy.all import IP, ICMP, Raw, send

def generate_icmp_packet(dest_ip, num_packets, payload=None):
    # Generate ICMP packets using Scapy.

    packets = []
    
    for _ in range(num_packets):
        # Create the ICMP packet
        icmp_packet = IP(dst=dest_ip) / ICMP()  # Basic ICMP Echo Request (Ping) packet
        
        # Add payload if provided
        if payload:
            icmp_packet = icmp_packet / Raw(load=payload)
        
        # Append packet to the list
        packets.append(icmp_packet)
        
        # Send the packet
        send(icmp_packet, verbose=0)  # Sending the ICMP packet

    return packets
# Function to render text
def draw_title(text, font, color, x, y):
    title_surface = font.render(text, True, color)
    screen.blit(title_surface, (x, y))

# Function to draw rounded rectangle
def draw_rounded_rect(surface, rect, color, radius):
    rounded_rect_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(rounded_rect_surface, color, (0, 0, rect.width, rect.height), border_radius=radius)
    surface.blit(rounded_rect_surface, rect.topleft)

# Custom button function
def draw_button(text, rect, font):
    draw_rounded_rect(screen, rect, BUTTON_COLOR, 20)  # 20 is the corner radius
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Mansion video playback using MoviePy
def play_mansion_video():
    video = moviepy.VideoFileClip("gamemedia/mansionvideo.mp4")
    video.preview()  # Open a preview window to play the video
    video.close()
import sys
import re

def is_valid_ip(ip):
    """Validate the entered IP address format."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def is_correct_ip(ip):
    """Check if the IP address matches the required value."""
    return ip == "10.23.90.2"

def ip_search_window():
    next_running = True
    input_box = pygame.Rect(250, 350, 300, 30)  # Input box dimensions
    input_color_inactive = (200, 200, 200)  # Inactive input box color
    input_color_active = (255, 255, 255)  # Active input box color
    input_color = input_color_inactive
    user_text = ""  # To store the text entered by the user
    active = False  # Input box starts inactive
    mac_address = ""  # To display the MAC address
    error_message = ""  # To store error message

    # Button rectangles for Back and Next
    back_button_rect = pygame.Rect(15, 530, 100, 35)
    next_button_rect = pygame.Rect(680, 530, 100, 35)

    while next_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on the input box or buttons
                pos = pygame.mouse.get_pos()
                if input_box.collidepoint(pos):
                    active = True
                    input_color = input_color_active
                else:
                    active = False
                    input_color = input_color_inactive

                if back_button_rect.collidepoint(pos):
                    next_running = False  # Go back to the previous window (basic_level or level_selection_menu)
                elif next_button_rect.collidepoint(pos):
                    # Validate IP address before proceeding
                    if is_valid_ip(user_text):
                        error_message = ""  # Clear any previous error
                        case_followup_window()
                        print("You successfully found device")
                    else:
                        error_message = "Invalid IP address. Please try again!"

            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    if is_correct_ip(user_text):
                        mac_address = get_local_mac()  # Retrieve MAC address when Enter is pressed
                        error_message = ""  # Clear error
                    else:
                        error_message = "Invalid IP address. Please try again!"
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]  # Remove the last character
                else:
                    user_text += event.unicode  # Add typed character

        # Draw the window
        screen.blit(bonus_background, (0, 0))  # Background
        draw_title("Welcome Sherlock", haunted_font, TEXT_COLOR, 250, 20)
        draw_title("The Hartley Mansion LAN", haunted_font, TEXT_COLOR, 200, 75)

        draw_title("What device would you like to find?", vintage_rotter_font, TEXT_COLOR, 200, 300)

        # Draw the input box
        pygame.draw.rect(screen, input_color, input_box)
        text_surface = arial_font.render(user_text, True, (0, 0, 0))  # Black text
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))  # Slight padding
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)  # Border for input box

        # Display the MAC address
        if mac_address:
            draw_title(f"Device MAC Address: {mac_address}", arial_font, (238, 75, 43), 220, 400)

        # Display error message if any
        if error_message:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(200, 450, 400, 50))
            error_surface = arial_font.render(error_message, True, (255, 255, 255))  # White text
            screen.blit(error_surface, (210, 460))  # Position the error message

        # Draw back and next buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Next", next_button_rect, vintage_rotter_font)

        pygame.display.update()
def basic_level():
    level_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)  # Position of back button
    next_button_rect = pygame.Rect(680, 530, 100, 35)  # Position of next button

    level_messages = [
        "At the heart of the mansion was the study", 
        "where Lord Gregory Hartley had been found—dead",
        "The only clue, a black envelope,", 
        "gripped tightly in his lifeless hand. No weapon in sight,",
        "no clear answers to the mystery. The envelope contained a",
        "cryptic message: 'Your sins will find you out. 10.23.90.2'",
        "The household staff were left in fear,",
        "----------------------------------------------",
        "Sherlock is brought in to solve the case.",
        "utilizing information on the envelope,",
        "which only had an IP address on it, he must now",
        "trackdown the device it belongs to.",
        "Will the owner be our killer? he asks lady Hartley",
    ]

    while level_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    level_running = False  # Exit the level
                elif next_button_rect.collidepoint(pos):
                    ip_search_window()  # Transition to the next window

        # Display the basic level interface
        screen.blit(bonus_background, (0, 0))
        draw_title("How Does ARP Work", roboto_font, TEXT_COLOR, 200, 50)

        y_offset = 140
        for line in level_messages:
            message_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(message_surface, (100, y_offset))
            y_offset += 35

        # Draw back and next buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Next", next_button_rect, vintage_rotter_font)

        pygame.display.update()

def case_followup_window():
    case_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)  # Back button position
    next_button_rect = pygame.Rect(680, 530, 100, 35)  # Next button position

    case_message = [
        "Although this solves the case of the envelope clue",
        "it does not solve the murder. Desperate to find a link",
        "between the device and the murder, Sherlock then continues",
        "to question members of the compound when he finds out...",
        "Lady Evelyn and Colonel Montgomery, had a secret affair.",
        "Is this a murder for love? He wonders….",

    ]

    while case_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    case_running = False  # Exit the window
                elif next_button_rect.collidepoint(pos):
                    # Continue to the next section or level
                    Spoof_check_window()

        # Draw the case follow-up window background
        screen.blit(bonus_background, (0, 0))

        # Display the case text
        draw_title("Case Follow-Up", haunted_font, TEXT_COLOR, 250, 50)

        y_offset = 140
        for line in case_message:
            message_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(message_surface, (100, y_offset))
            y_offset += 35

        # Draw back and next buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Next", next_button_rect, vintage_rotter_font)

        pygame.display.update()

def Spoof_check_window():
    spoof_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)  # Back button position
    next_button_rect = pygame.Rect(680, 530, 100, 35)  # Next button position

    spoof_message = [
        "Conflicted with the new found information about LOVE",
        "Sherlock takes an extra measure to ensure the information",
        "from the Mansions device retrieval system is not",
        "in any way compromised",
        "As the killer may be giving false responses and", 
        "intercepting the correct data",

    ]

    while spoof_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    spoof_running = False  # Exit the window
                elif next_button_rect.collidepoint(pos):
                    # Continue to the next section or level
                    Evelyn_caught_window()
                    print("Moving to the next section...")

        # Draw the case follow-up window background
        screen.blit(bonus_background, (0, 0))

        # Display the case text
        draw_title("Is this Information Reliable", haunted_font, TEXT_COLOR, 200, 50)

        y_offset = 140
        for line in spoof_message:
            message_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(message_surface, (100, y_offset))
            y_offset += 35

        # Draw back and next buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Next", next_button_rect, vintage_rotter_font)

        pygame.display.update()

def Evelyn_caught_window():
    spoof_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)  # Back button position
    next_button_rect = pygame.Rect(680, 530, 100, 35)  # Next button position

    spoof_message = [
        "With the current imbalance holmes must now take a step back",
        "to ensure his investigation has not tampered with.",
        "Holmes sets a trap....",
        "He announces to the household that he’s found new evidence",
        "in his analysis,",
        "planning on re-requesting the IP address mapping to confirm",
        "all his data up to now is up to date.",
        "That evening, Lady Evelyn sent in a new ARP response from",
        "the study computer thinking everyone was asleep", 
        "exactly as Holmes predicted",
        "Holmes had placed a camera in the room",
        "as well as a monitoring software",
        "to record activity of all home network devices",
    ]

    while spoof_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    spoof_running = False  # Exit the window
                elif next_button_rect.collidepoint(pos):
                    # Continue to the next section or level
                    Confrontation_window()
                    print("Moving to the next section...")

        # Draw the case follow-up window background
        screen.blit(bonus_background, (0, 0))

        # Display the case text
        draw_title("Checking the network", haunted_font, TEXT_COLOR, 200, 50)

        y_offset = 140
        for line in spoof_message:
            message_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(message_surface, (100, y_offset))
            y_offset += 35

        # Draw back and next buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Next", next_button_rect, vintage_rotter_font)

        pygame.display.update()


def Confrontation_window():
    spoof_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)  # Back button position
    next_button_rect = pygame.Rect(680, 530, 100, 35)  # Next button position

    spoof_message = [
        "Holmes confronts her and she confesses.",
         "Her confession: after discovering her husband had planned",
         "to expose her affair and ruin her name",
         "she shot him in a panic, leaving the black envelope", 
         "to mislead investigators. Her desperate attempt to", 
         "conceal the truth got her caught.",
         "Evelyn was soon arrested, and sentenced to 30 yrs in jail.",
         "Evelyn is curently registered at 8.8.8.8",
         "Try sending her a message with the Contact protal.",
    ]

    while spoof_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    spoof_running = False  # Exit the window
                elif next_button_rect.collidepoint(pos):
                    # Continue to the next section or level
                    After_Effect_window()
                    print("Moving to the next section...")

        # Draw the case follow-up window background
        screen.blit(bonus_background, (0, 0))

        # Display the case text
        draw_title("The Confrontation", haunted_font, TEXT_COLOR, 200, 50)

        y_offset = 140
        for line in spoof_message:
            message_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(message_surface, (100, y_offset))
            y_offset += 35

        # Draw back and next buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Next", next_button_rect, vintage_rotter_font)

        pygame.display.update()

def After_Effect_window():
    spoof_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)  # Back button position
    next_button_rect = pygame.Rect(500, 530, 100, 35)  # Next button position

    spoof_message = [
        "With the loss of a family member and one in jail,",
        "Sherlock was moved to help the family",
        "Make their Network more secure against ARP Spoofing,",
        "He suggested anti-ARP spoofing software and encryption",
        "Use of static ARP⁠, which lets you define a static",
        "ARP entry for an IP address, and prevent devices",
        "from listening on ARP responses for that address.",
        "All at no extra cost!!!",
    ]

    while spoof_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    spoof_running = False  # Exit the window
                elif next_button_rect.collidepoint(pos):
                    # Continue to the next section or level
                    intermediate_level_window()
                    print("The End")

        # Draw the case follow-up window background
        screen.blit(bonus_background, (0, 0))

        # Display the case text
        draw_title("Way Forward", haunted_font, TEXT_COLOR, 200, 50)

        y_offset = 140
        for line in spoof_message:
            message_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(message_surface, (100, y_offset))
            y_offset += 35

        # Draw back and next buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("THE END", next_button_rect, vintage_rotter_font)

        pygame.display.update()
# Placeholder function for level selection
def level_selection_menu():
    selection_running = True
    buttons = {
        'Basic': pygame.Rect(330, 220, 150, 35),
        'Contact Portal': pygame.Rect(330, 330, 150, 35),
        'back': pygame.Rect(15, 530, 100, 35),
    }

    while selection_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if buttons['Basic'].collidepoint(pos):
                    basic_level()
                elif buttons['Contact Portal'].collidepoint(pos):
                    intermediate_level_window()
                elif buttons['back'].collidepoint(pos):
                    selection_running = False

        screen.blit(glossary_background, (0, 0))
        draw_title("Select Level", haunted_font, TEXT_COLOR, 260, 50)
        for button_text, rect in buttons.items():
            draw_button(button_text.capitalize(), rect, vintage_rotter_font)

        pygame.display.update()

# Define button rectangles
button_rects = {
    'Start': pygame.Rect(350, 220, 100, 35),
    'Select Level': pygame.Rect(330, 330, 150, 35),
    'Bonus': pygame.Rect(330, 430, 150, 35),
    'Credits': pygame.Rect(640, 530, 150, 35),
    'Quit': pygame.Rect(15, 530, 100, 35)
}

import re

def is_valid_ip(ip):
    """Validate IP address format."""
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if pattern.match(ip):
        parts = ip.split(".")
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def intermediate_level_window():
    running = True
    input_boxes = {
        'packet_count': pygame.Rect(450, 150, 300, 30),
        'payload': pygame.Rect(450, 200, 300, 30),
        'dest_ip': pygame.Rect(450, 250, 300, 30),
    }
    input_texts = {'packet_count': '', 'payload': '', 'dest_ip': ''}
    input_colors = {key: (200, 200, 200) for key in input_boxes}  # Default inactive colors
    active_box = None  # Tracks the currently active input box

    # Protocol Dropdown
    protocol_dropdown = pygame.Rect(250, 350, 300, 30)
    protocol_options = ['ARP', 'ICMP']
    selected_protocol = protocol_options[0]
    dropdown_active = False

    # Back and Generate buttons
    back_button_rect = pygame.Rect(15, 530, 100, 35)
    generate_button_rect = pygame.Rect(680, 530, 100, 35)

    # Error messages
    error_message = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which input box (if any) was clicked
                for key, box in input_boxes.items():
                    if box.collidepoint(event.pos):
                        active_box = key
                        input_colors[key] = (255, 255, 255)  # Active color
                    else:
                        input_colors[key] = (200, 200, 200)  # Inactive color

                # Check for dropdown click
                if protocol_dropdown.collidepoint(event.pos):
                    dropdown_active = not dropdown_active  # Toggle dropdown
                elif dropdown_active:
                    for i, option in enumerate(protocol_options):
                        option_rect = pygame.Rect(protocol_dropdown.x, protocol_dropdown.y + (i + 1) * 30, protocol_dropdown.width, 30)
                        if option_rect.collidepoint(event.pos):
                            selected_protocol = option
                            dropdown_active = False
                            break

                # Handle button clicks
                if back_button_rect.collidepoint(event.pos):
                    return  # Go back to the previous window
                elif generate_button_rect.collidepoint(event.pos):
                    # Use the inputs and selected protocol
                    packet_count = input_texts['packet_count']
                    payload = input_texts['payload']
                    dest_ip = input_texts['dest_ip']

                    # Validate inputs
                    if not packet_count.isdigit() or not (1 <= int(packet_count) <= 1000):
                        error_message = "Packet count must be a number between 1 and 1000."
                        continue
                    if not is_valid_ip(dest_ip):
                        error_message = "Invalid IP address format."
                        continue

                    error_message = ""  # Clear any previous errors

                    if selected_protocol == 'ARP':
                        packets = generate_arp_packet(dest_ip, int(packet_count), payload.encode() if payload else None)
                        print("Generated ARP packets:", packets)
                    elif selected_protocol == 'ICMP':
                        packets = generate_ip_packet(dest_ip, int(packet_count), payload.encode() if payload else None)
                        print("ICMP packet generation placeholder")

            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_RETURN:
                    active_box = None  # Deselect the box on Enter
                elif event.key == pygame.K_BACKSPACE:
                    input_texts[active_box] = input_texts[active_box][:-1]
                else:
                    input_texts[active_box] += event.unicode

        # Draw the window
        screen.blit(bonus_background, (0, 0))  # Background
        draw_title("Inmate Contact Portal", haunted_font, TEXT_COLOR, 150, 50)

        # Draw input boxes and their labels
        draw_title("Message (Packet) Count:", arial_font, TEXT_COLOR, 100, 150)
        draw_title("Message (Payload):", arial_font, TEXT_COLOR, 100, 200)
        draw_title("Inmate Location (Destination IP):", arial_font, TEXT_COLOR, 100, 250)
        draw_title("How would you like to contact inmate (protocol):", arial_font, TEXT_COLOR, 100, 300)

        for key, box in input_boxes.items():
            pygame.draw.rect(screen, input_colors[key], box)
            text_surface = arial_font.render(input_texts[key], True, (0, 0, 0))  # Black text
            screen.blit(text_surface, (box.x + 5, box.y + 5))  # Slight padding
            pygame.draw.rect(screen, (0, 0, 0), box, 2)  # Border

        # Draw protocol dropdown
        pygame.draw.rect(screen, (200, 200, 200), protocol_dropdown)  # Dropdown box
        text_surface = arial_font.render(selected_protocol, True, (0, 0, 0))  # Black text
        screen.blit(text_surface, (protocol_dropdown.x + 5, protocol_dropdown.y + 5))  # Padding
        pygame.draw.rect(screen, (0, 0, 0), protocol_dropdown, 2)  # Border

        if dropdown_active:
            for i, option in enumerate(protocol_options):
                option_rect = pygame.Rect(protocol_dropdown.x, protocol_dropdown.y + (i + 1) * 30, protocol_dropdown.width, 30)
                pygame.draw.rect(screen, (200, 200, 200), option_rect)
                option_surface = arial_font.render(option, True, (0, 0, 0))  # Black text
                screen.blit(option_surface, (option_rect.x + 5, option_rect.y + 5))
                pygame.draw.rect(screen, (0, 0, 0), option_rect, 2)  # Border

        # Draw error message if any
        if error_message:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(100, 500, 600, 30))  # Red background for error
            error_surface = arial_font.render(error_message, True, (255, 255, 255))  # White text
            screen.blit(error_surface, (110, 505))

        # Draw Back and Generate buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Generate", generate_button_rect, vintage_rotter_font)

        pygame.display.update()

def show_bonus():
    bonus_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)
    glossary_button_rect = pygame.Rect(640, 530, 150, 35)

    small_font = pygame.font.Font(r'Fonts\vintage_rotter.otf', 30)  # Smaller font for bonus text

    while bonus_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bonus_running = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    bonus_running = False
                elif glossary_button_rect.collidepoint(pos):
                    show_glossary()  # Call glossary function

        # Draw bonus background
        screen.blit(bonus_background, (0, 0))

        # Draw bonus title
        draw_title("Bonus Content", haunted_font, TEXT_COLOR, 260, 50)

        # Display bonus information
        bonus_info = [
            "Explore ARP (Address Resolution Protocol) Basics:",
            "- ARP helps devices find each other's MAC addresses in a network",
            "- Devices send an ARP request: 'Who owns this IP address?'",
            "- The owner replies with its MAC address",
            "- This mapping is saved in an ARP cache for quick use",
            "",
            "Why is ARP important?",
            "- It ensures smooth communication in a local network",
            "- It connects devices using MAC addresses while",
            "  IP addresses handle routing",
            "Learn how devices talk and exchange information efficiently!"
        ]
        y_offset = 150
        for line in bonus_info:
            text_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 35  # Adjust line spacing

        # Draw the buttons
        draw_button("Back", back_button_rect, vintage_rotter_font)
        draw_button("Glossary", glossary_button_rect, vintage_rotter_font)

        pygame.display.update()

# Function to display glossary
def show_glossary():
    glossary_running = True
    back_button_rect = pygame.Rect(640, 530, 150, 35)
    small_font = pygame.font.Font(r'Fonts\vintage_rotter.otf', 25)  # Smaller font for glossary content

    glossary_text = [
        "ARP Terminology Simplified:",
        "ARP (Address Resolution Protocol):",
        "- A protocol to match an IP address with a MAC address",
        "IP Address (Internet Protocol Address):",
        "- A unique number to identify devices in a network",
        "MAC Address (Media Access Control Address):",
        "- A hardware ID for communication in a local network",
        "ARP Cache:",
        "- A temporary table storing IP-to-MAC mappings",
        "ARP Request:",
        "- A message asking 'Who owns this IP address?'",
        "ARP Reply:",
        "- The answer: 'This is my MAC address'",
        "Broadcast:",
        "- A message sent to all devices in the local network",
        "Unicast:",
        "- A message sent directly to one specific device",
        "LAN (Local Area Network):",
        "- A small network in a home office or campus",
        "Protocol:",
        "- Rules that help devices communicate efficiently"
    ]

    while glossary_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                glossary_running = False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    glossary_running = False

        # Draw glossary background
        screen.blit(glossary_background, (0, 0))

        # Draw glossary title
        draw_title("Glossary", haunted_font, TEXT_COLOR, 260, 50)

        # Display glossary content
        y_offset = 120
        for line in glossary_text:
            text_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(text_surface, (120, y_offset))
            y_offset += 25  # Adjust line spacing

        # Draw the back button
        draw_button("Back", back_button_rect, vintage_rotter_font)

        pygame.display.update()

# Function to display credits
def show_credits():
    credits_running = True
    back_button_rect = pygame.Rect(15, 530, 100, 35)
    small_font = pygame.font.Font(r'Fonts\vintage_rotter.otf', 30)

    credits_text = [
        " ",
        "Author: Anwuli Ajabor",
        "Concept: Interactive learning process for ARP,", 
        "and packet generation for ARP, ICMP,",
        "in network protocols and cybersecurity",
        "Hope you enjoy the experience!",
    ]

    while credits_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                credits_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(pos):
                    credits_running = False

        # Draw credits background
        screen.blit(glossary_background, (0, 0))

        # Draw credits title
        draw_title("Credits", haunted_font, TEXT_COLOR, 300, 50)

        # Display credits information
        y_offset = 120
        for line in credits_text:
            text_surface = arial_font.render(line, True, TEXT_COLOR)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 35

        # Draw the back button
        draw_button("Back", back_button_rect, vintage_rotter_font)

        pygame.display.update()

# Main loop for the start screen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if button_rects['Start'].collidepoint(pos):
                play_mansion_video()
                basic_level()
                print("Starting the game...")
                # Add game start logic here
            elif button_rects['Select Level'].collidepoint(pos):
                level_selection_menu()
            elif button_rects['Bonus'].collidepoint(pos):
                show_bonus()
            elif button_rects['Credits'].collidepoint(pos):
                show_credits()  # Show credits in a new window
            elif button_rects['Quit'].collidepoint(pos):
                pygame.quit()
                sys.exit()

    # Draw the start screen
    screen.blit(background, (0, 0))
    draw_title("The Mac Murderer", haunted_font, TEXT_COLOR, 250, 50)
    for button_text, rect in button_rects.items():
        draw_button(button_text, rect, vintage_rotter_font)

    pygame.display.update()
    clock.tick(60)
