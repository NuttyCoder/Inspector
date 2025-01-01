import nmap

def scan_network():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.68.0/24', arguments='-sn')  # Adjust this range for your network
    devices = []
    for host in nm.all_hosts():
        device = {
            'host': host,
            'hostname': nm[host].hostname(),
            'state': nm[host].state(),
        }
        devices.append(device)
    return devices

if __name__ == "__main__":
    devices = scan_network()
    print("Devices found:", devices)
