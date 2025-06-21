import socket

# This function scans TCP ports within a specified range on a given IPv4 address.
# This script does not use threading, so it scans ports one by one and may be slow if scanning many ports.

def scan_ports(target_ip, start_port, end_port):
    print("Scanning", target_ip, "from port", start_port, "to", end_port)
    # A list is created to store open ports.
    open_ports = list()
    for port in range(start_port, end_port + 1):
        # This helps track the scanning progress.
        print("Scanning port", port)
        # A socket is created for each port and attempts to connect.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # A timeout is set for the connection attempt.
            sock.settimeout(0.5)
            # Attempts to connect to the specified port.
            result = sock.connect_ex((target_ip, port))
            # If there is no error (result == 0), the port is open.
            if result == 0:
                # The port is added to the list of open ports.
                print("Port", port, "open")
                open_ports.append(port)
    if open_ports:
        print("Open ports:", open_ports)
    else:
        print("No open ports found.")

# Ensures the script runs only if executed directly.
if __name__ == "__main__":
    ip = input("Which IPv4 address do you want to scan? ")
    start_port = int(input("From which port do you want to start? "))
    end_port = int(input("To which port do you want to scan? "))
    scan_ports(ip, start_port, end_port)
