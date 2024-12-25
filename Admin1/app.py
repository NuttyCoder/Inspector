from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = database.get_users()
        user = next((u for u in users if u[1] == username and u[2] == password), None)
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            if user[3] == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                return redirect(url_for('user_panel'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/admin_panel')
def admin_panel():
    if 'role' in session and session['role'] == 'admin':
        users = database.get_users()
        return render_template('admin_panel.html', users=users)
    return redirect(url_for('login'))

@app.route('/user_panel')
def user_panel():
    if 'role' in session and session['role'] == 'user':
        return render_template('user_panel.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
