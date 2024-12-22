from flask import Flask, request, render_template, jsonify
import scanner
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    file_path = os.path.join('/tmp', file.filename)
    file.save(file_path)
    scan_result = scanner.scan_file(file_path)
    os.remove(file_path)
    return render_template('results.html', scan_result=scan_result, file_name=file.filename)

@app.route('/scan_directory', methods=['POST'])
def scan_directory():
    directory_path = request.form['directory_path']
    scan_result = scanner.scan_directory(directory_path)
    return jsonify(scan_result)

if __name__ == '__main__':
    app.run(debug=True)
