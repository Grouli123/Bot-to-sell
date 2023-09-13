import sqlite3
import threading
import time
from typing import Callable

# Функция, которая будет вызываться при записи в базу данных
def on_database_write():
    # Подключение к базе данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Получение новых данных из базы данных
    cursor.execute('SELECT * FROM table')
    data = cursor.fetchall()

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Передача данных в другой скрипт
    process_data(data)

# Функция для обработки данных
def process_data(data):
    # Вывод данных в консоли
    for row in data:
        print(row)

# Подписка на событие записи в базу данных
def subscribe_to_database_write(callback: Callable):
    def check_database_changes():
        # Проверка изменений в базе данных
        while True:
            # Ожидание определенного интервала времени
            time.sleep(1)

            # Проверка наличия новых записей в базе данных
            has_changes = check_for_database_changes()

            # Если есть изменения, вызываем обратный вызов
            if has_changes:
                callback()

    # Запуск потока для проверки изменений в базе данных
    thread = threading.Thread(target=check_database_changes)
    thread.start()

# Функция для проверки наличия новых записей в базе данных
def check_for_database_changes():
    # Подключение к базе данных
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Проверка наличия новых записей
    cursor.execute('SELECT COUNT(*) FROM table')
    count = cursor.fetchone()[0]

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

    # Если количество записей больше 0, есть изменения
    return count > 0

# Пример использования
subscribe_to_database_write(on_database_write)