import subprocess

# Список путей к скриптам, которые нужно запустить
script_paths = [
    'admin_main.py',
    'get_orders_mainArzamas.py',
    'registration_main.py',
    'OrdersAdmin.py',
    'get_orders_mainSPB.py',
    'get_orders_mainMoskow.py',
    'get_orders_mainEka.py'
]

# Список для хранения процессов
processes = []

# Запускаем каждый скрипт в отдельном процессе
for script_path in script_paths:
    process = subprocess.Popen(['python3', script_path])
    processes.append(process)

# Дожидаемся завершения всех процессов
for process in processes:
    process.wait()