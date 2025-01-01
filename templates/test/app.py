from flask import Flask, jsonify
import nmap

app = Flask(__name__)

def scan_network():
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.68.110', arguments='-sn --unprivileged')
        print("Scan info:", nm.scaninfo())
        devices = []
        for host in nm.all_hosts():
            device = {
                'host': host,
                'hostname': nm[host].hostname(),
                'state': nm[host].state(),
                'mac': nm[host]['addresses'].get('mac', 'N/A'),
                'vendor': nm[host]['vendor'].get(nm[host]['addresses'].get('mac', ''), 'N/A')
            }
            devices.append(device)
        print("Devices found:", devices)
        return devices
    except Exception as e:
        print("Error scanning devices:", e)
        return []

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/api/devices', methods=['GET'])
def get_connected_devices():
    print("Endpoint reached: /api/devices")
    devices = scan_network()
    print("Devices returned:", devices)
    return jsonify(devices)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
