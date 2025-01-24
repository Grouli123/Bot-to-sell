from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Секретный ключ для сессий

# Функция для подключения к базе данных
def connect_db(db_name):
    if not os.path.exists(db_name):
        raise FileNotFoundError(f"Database {db_name} does not exist.")
    return sqlite3.connect(db_name)

# Главная страница приложения
@app.route('/')
def index():
    session.pop('logged_in', None)  # Удалить авторизацию при открытии сайта
    return render_template('login.html')

# Обработка формы логина
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'admin' and password == 'admin123':
        session['logged_in'] = True
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Неверный логин или пароль")

# Страница после успешного входа
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

# API для получения данных из базы данных
@app.route('/api/data', methods=['GET'])
def get_data():
    if 'logged_in' not in session or not session['logged_in']:
        return {"error": "Unauthorized"}, 401

    db_name = request.args.get('db')
    table_name = request.args.get('table')

    if not db_name or not table_name:
        return {"error": "Missing 'db' or 'table' parameter"}, 400

    try:
        conn = connect_db(db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        conn.close()

        return {"records": records}
    except Exception as e:
        return {"error": str(e)}, 500

# API для обновления подписки
@app.route('/api/subscription', methods=['POST'])
def update_subscription():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        customer_id = request.args.get('customer_id')
        action = request.args.get('action')

        if not customer_id or not action:
            return jsonify({"error": "Missing 'customer_id' or 'action' parameter"}), 400

        new_status = 'true' if action == 'activate' else 'false'

        conn = connect_db('custumers.sql')
        cursor = conn.cursor()
        cursor.execute("UPDATE custumers SET podpiska = ? WHERE id = ?", (new_status, customer_id))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "new_status": new_status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Выход из системы
@app.route('/logout', methods=['POST'])  # Убедитесь, что здесь указан POST
def logout():
    # Удалить сессию пользователя
    session.pop('logged_in', None)
    return redirect(url_for('index'))  # Перенаправление на страницу входа


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)