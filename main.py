import socket
import argparse
import concurrent.futures

def scan_port(host, port, scan_type, timeout=3, verbose=False):
    """Scans a specific port on a given host."""
    try:
        if verbose:
            print(f"Scanning {host}:{port} ({scan_type.upper()})...")
        
        if scan_type == "tcp":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            s.close()
            return result == 0
        elif scan_type == "udp":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(timeout)
            s.sendto(b"", (host, port))
            try:
                s.recvfrom(1024)
                return True
            except socket.timeout:
                return "possibly open but unresponsive"
    except Exception as e:
        if verbose:
            print(f"Error scanning {host}:{port} - {e}")
        return False

def get_service_name(port, scan_type):
    """Returns the service name for a given port."""
    try:
        if scan_type == "tcp":
            return socket.getservbyport(port, "tcp")
        elif scan_type == "udp":
            return socket.getservbyport(port, "udp")
    except OSError:
        return "Unknown"

def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("host", help="Target host IP address")
    parser.add_argument("-p", "--port", required=True, help="Port or range of ports to scan (e.g., 80 or 20-100)")
    parser.add_argument("-t", "--tcp", action="store_true", help="Perform a TCP scan")
    parser.add_argument("-u", "--udp", action="store_true", help="Perform a UDP scan")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode for debugging")
    
    args = parser.parse_args()
    scan_type = "tcp" if args.tcp else "udp"
    verbose = args.verbose
    
    if "-" in args.port:
        start_port, end_port = map(int, args.port.split("-"))
        ports = range(start_port, end_port + 1)
    else:
        ports = [int(args.port)]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_port = {executor.submit(scan_port, args.host, port, scan_type, 3, verbose): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                is_open = future.result()
                service = get_service_name(port, scan_type)
                status = "open" if is_open else "closed" if is_open is False else is_open
                print(f"Port {port} ({service}) is {status}")
            except Exception as e:
                print(f"Port {port}: Error - {e}")

if __name__ == "__main__":
    main()
