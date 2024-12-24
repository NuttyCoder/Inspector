from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

def validate_input(data):
    # Add validation logic (e.g., check data types, length)
    return True

@app.route('/add_user', methods=['POST'])
def add_user():
    user_id = request.form['user_id']
    username = request.form['username']
    
    if validate_input(user_id) and validate_input(username):
        # Use parameterized queries to prevent SQL injection
        conn = sqlite3.connect('xbox_usage.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User added successfully!'})
    else:
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)
