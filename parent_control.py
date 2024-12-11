from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

devices = {}  # Dictionary to store device information

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/register', methods=['POST'])
def register_device():
    user_id = request.json.get('user_id')
    device = request.json.get('device')
    if user_id not in devices:
        devices[user_id] = []
    devices[user_id].append(device)
    return jsonify({'message': 'Device registered successfully'}), 200

@app.route('/devices/<user_id>', methods=['GET'])
def get_devices(user_id):
    user_devices = devices.get(user_id, [])
    return jsonify({'devices': user_devices}), 200

@app.route('/set_time_limit', methods=['POST'])
def set_time_limit():
    user_id = request.json.get('user_id')
    device_ip = request.json.get('device_ip')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')

    # Use iptables to schedule internet access
    command = f"iptables -A INPUT -s {device_ip} -m time --timestart {start_time} --timestop {end_time} -j ACCEPT"
    subprocess.run(command, shell=True)

    return jsonify({'message': 'Time limit set successfully'}), 200

@app.route('/block_website', methods=['POST'])
def block_website():
    website = request.json.get('website')

    # Add website to dnsmasq config
    with open
