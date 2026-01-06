import os
import time
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'devops')

mysql = MySQL(app)

def init_db(retries=10, delay=3):
    for i in range(retries):
        try:
            with app.app_context():
                cur = mysql.connection.cursor()
                cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    message TEXT
                );
                """)
                mysql.connection.commit()
                cur.close()
                print("Database initialized")
                return
        except Exception as e:
            print(f"DB not ready, retrying {i+1}/{retries}...")
            time.sleep(delay)
    raise RuntimeError("Database never became available")

@app.before_first_request
def setup():
    init_db()

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/')
def hello():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': new_message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
