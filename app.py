from flask import Flask, jsonify, send_from_directory, request, abort
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
CORS(app)
db_config = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "database": os.getenv('DB_DATABASE'),
    "port": os.getenv('DB_PORT')
}
def load_credentials():
    credentials = []
    for key, value in os.environ.items():
        if key.startswith("USER_"):
            user_number = key.split("_")[1]
            password_key = f"PASSWORD_{user_number}"
            password = os.getenv(password_key)
            if password:
                credentials.append((value, password))
    return credentials
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn
@app.route('/api/data', methods=['GET'])
def get_area():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM area")
    areas = cursor.fetchall()
    conn.close()
    return jsonify(areas)
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')
@app.route('/edit')
def edit():
    return send_from_directory('static', 'edit.html')
@app.route('/api/update', methods=['POST'])
def update_area():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    area_id = data.get('id')
    new_name = data.get('name')
    new_info = data.get('info')
    new_status = data.get('status')
    new_detail = data.get('detail')
    new_color = data.get('color')
    valid_credentials = load_credentials()
    if not any(username == user and password == pwd for user, pwd in valid_credentials):
        return jsonify({"message": "账号或密码错误"}), 401
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE area SET name = %s, info = %s, status = %s, detail = %s, color = %s WHERE id = %s",
            (new_name, new_info, new_status, new_detail, new_color, area_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        abort(500, str(e))
    finally:
        conn.close()
    return jsonify({"message": "成功"})
@app.route('/api/get/<int:id>', methods=['GET'])
def get_area_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM area WHERE id = %s", (id,))
    area = cursor.fetchone()
    conn.close()
    if not area:
        abort(404, "ID未找到")
    return jsonify(area)
if __name__ == '__main__':
    app.run(debug=True)