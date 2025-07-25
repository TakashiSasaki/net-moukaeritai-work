import socket
import urllib.request
import xml.etree.ElementTree as ET

# SSDPマルチキャストアドレスとポート
SSDP_MULTICAST_ADDRESS = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 2
SSDP_ST = "ssdp:all"  # ディスカバリーするための検索ターゲット

# SSDPディスカバリメッセージ
ssdp_discover_message = (
    f"M-SEARCH * HTTP/1.1\r\n"
    f"HOST: {SSDP_MULTICAST_ADDRESS}:{SSDP_PORT}\r\n"
    f"MAN: \"ssdp:discover\"\r\n"
    f"MX: {SSDP_MX}\r\n"
    f"ST: {SSDP_ST}\r\n"
    f"\r\n"
)

# SSDPソケットの作成と設定
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.settimeout(100)  # タイムアウトを10秒に設定

# マルチキャストアドレスへのディスカバリメッセージの送信
sock.sendto(ssdp_discover_message.encode(), (SSDP_MULTICAST_ADDRESS, SSDP_PORT))

# レスポンスの受信と表示
try:
    while True:
        data, addr = sock.recvfrom(65507)
        print(f"Received response from {addr}:\n{data.decode()}\n")

        # ロケーションURLの抽出
        response_lines = data.decode().split("\r\n")
        location_url = None
        for line in response_lines:
            if line.lower().startswith("location:"):
                location_url = line.split(":", 1)[1].strip()
                break
        
        if location_url:
            print(f"Location URL: {location_url}")
            # デバイスの説明XMLを取得して表示
            try:
                with urllib.request.urlopen(location_url) as response:
                    description_xml = response.read()
                    tree = ET.ElementTree(ET.fromstring(description_xml))
                    root = tree.getroot()
                    print(ET.tostring(root, encoding="unicode"))
            except Exception as e:
                print(f"Failed to retrieve description XML: {e}")
except socket.timeout:
    print("Discovery process completed.")

sock.close()
