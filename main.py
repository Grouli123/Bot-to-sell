import subprocess

# Список путей к скриптам, которые нужно запустить
script_paths = [
    'admin_main.py',
    'get_orders_main.py',
    'registration_main.py',
    'OrdersAdmin.py'
    # 'openTest.py',
    # 'observable.py',
    # 'observer.py'
    # 'test.py',
    # 'moskow_get_orders_main.py'
]

# Список для хранения процессов
processes = []

# Запускаем каждый скрипт в отдельном процессе
for script_path in script_paths:
    process = subprocess.Popen(['python', script_path])
    processes.append(process)

# Дожидаемся завершения всех процессов
for process in processes:
    process.wait()