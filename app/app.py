from flask import Flask, request, make_response, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv
import socket
import traceback
import time

app = Flask(__name__)

# Database configuration from environment variables
load_dotenv()

db_config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DB'),
}

print(db_config)

# Initialize global counter
global_counter = 0

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Error: {e}")
            retries -= 1
            time.sleep(5)
    raise Exception("Failed to connect to the database after multiple attempts.")

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Increment the counter
        cursor.execute("UPDATE counter SET count = count + 1 WHERE id = 1")
        conn.commit()

        # Get the current counter value
        cursor.execute("SELECT count FROM counter WHERE id = 1")
        counter_value = cursor.fetchone()[0]

        # Get the internal IP address of the server
        internal_ip = socket.gethostbyname(socket.gethostname())
        print(f"Internal IP: {internal_ip}")

        # Get the server_ip cookie
        server_ip_cookie = request.cookies.get('server_ip')
        print(f"Existing server_ip cookie: {server_ip_cookie}")

        if not server_ip_cookie:
            # Set a new cookie with the internal IP address for 5 minutes
            print("Setting new server_ip cookie")
            resp = make_response(jsonify({'internal_ip': internal_ip, 'counter': counter_value}))
            resp.set_cookie('server_ip', internal_ip, max_age=300)  # 5 minutes
        else:
            # Use the existing cookie value
            print("Using existing server_ip cookie")
            resp = make_response(jsonify({'internal_ip': server_ip_cookie, 'counter': counter_value}))

        # Log access to the database
        client_ip = request.remote_addr
        now = datetime.now()
        cursor.execute(
            "INSERT INTO access_log (timestamp, client_ip, internal_ip) VALUES (%s, %s, %s)",
            (now, client_ip, internal_ip)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return resp
    except Exception as e:
        error_message = f"Error: {e}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({'error': 'Internal Server Error', 'details': error_message}), 500

@app.route('/showcount')
def showcount():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM counter WHERE id = 1")
        counter_value = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({'count': counter_value})
    except Exception as e:
        error_message = f"Error: {e}\n{traceback.format_exc()}"
        print(error_message)
        return jsonify({'error': 'Internal Server Error', 'details': error_message}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
