from flask import Flask, jsonify, request
from urllib.parse import quote as url_quote
import mysql.connector
import os

app = Flask(__name__)

# Configuration for MySQL
db_user = os.getenv('MYSQL_USER')
db_password = os.getenv('MYSQL_PASSWORD')
db_host = os.getenv('MYSQL_HOST', 'db')  # "db" is the service name in Docker Compose
db_name = os.getenv('MYSQL_DATABASE')

# Function to get a database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return connection

# Create the database tables if not exists
@app.before_request
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(80) NOT NULL
        );
    ''')
    connection.commit()
    cursor.close()
    connection.close()

# API route to add users
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (name) VALUES (%s)', (data['name'],))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'message': 'User added successfully!'})

# API route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
