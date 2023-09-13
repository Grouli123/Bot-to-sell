import testone
# Функция, которая будет вызываться при получении новых данных из базы данных
def process_data(data):
    # Вывод данных в консоли
    for row in data:
        print(row)

def subscribe_to_database_write(callback):
    callback()
# Подписка на событие записи в базу данных
    subscribe_to_database_write(process_data)