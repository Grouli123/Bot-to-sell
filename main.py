import subprocess

# Список путей к скриптам, которые нужно запустить
script_paths = [
    # 'test1.py',
    # 'test2.py',
    # 'test3.py'
    'admin_main.py',
    'get_orders_main.py',
    'registration_main.py'
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