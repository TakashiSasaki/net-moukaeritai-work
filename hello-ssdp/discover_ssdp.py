import socket
import http.client
from io import BytesIO

# A simple HTTP response parser that's good enough for SSDP
class SSDPResponse:
    def __init__(self, data):
        # The first line is the status line
        # The rest are headers
        # The body is empty
        rfile = BytesIO(data)
        line = rfile.readline().decode('utf-8').strip()
        parts = line.split(' ', 2)
        self.version = parts[0]
        self.status_code = int(parts[1])
        self.reason = parts[2]

        # Parse headers
        self.headers = http.client.parse_headers(rfile)

    def __repr__(self):
        return f'<SSDPResponse({self.status_code}, {self.reason})>'

def discover_ssdp_devices(timeout=2):
    """
    Discovers SSDP devices on the network.
    """
    ssdp_addr = "239.255.255.250"
    ssdp_port = 1900
    ssdp_mx = 1  # Seconds to delay response
    ssdp_st = "ssdp:all"  # Search target

    # M-SEARCH request message
    msearch_request = (
        f'M-SEARCH * HTTP/1.1\r\n'
        f'HOST: {ssdp_addr}:{ssdp_port}\r\n'
        f'MAN: "ssdp:discover"\r\n'
        f'MX: {ssdp_mx}\r\n'
        f'ST: {ssdp_st}\r\n'
        f'\r\n'
    ).encode('utf-8')

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(timeout)

    # Send the M-SEARCH request
    sock.sendto(msearch_request, (ssdp_addr, ssdp_port))

    print(f"Sent M-SEARCH, waiting for responses for {timeout} seconds...")

    devices = []
    try:
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                response = SSDPResponse(data)
                
                # We are only interested in OK responses
                if response.status_code == 200:
                    devices.append({
                        'location': response.headers.get('location'),
                        'server': response.headers.get('server'),
                        'st': response.headers.get('st'),
                        'usn': response.headers.get('usn'),
                        'addr': addr
                    })
            except socket.timeout:
                break
    finally:
        sock.close()

    return devices

if __name__ == "__main__":
    found_devices = discover_ssdp_devices()

    if found_devices:
        print(f"\nFound {len(found_devices)} SSDP devices:")
        for i, device in enumerate(found_devices, 1):
            print(f"--- Device {i} ---")
            print(f"  Address: {device['addr'][0]}:{device['addr'][1]}")
            print(f"  Location: {device['location']}")
            print(f"  Server: {device['server']}")
            print(f"  ST: {device['st']}")
            print(f"  USN: {device['usn']}")
    else:
        print("\nNo SSDP devices found on the network.")
