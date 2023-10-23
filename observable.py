class Observable:
    def __init__(self):
        self._value = "Исходное значение"
        self._observers = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        print(f"Текущее значение: {self._value}")
        self._value = new_value
        for observer in self._observers:
            observer.notify(new_value)

    def register_observer(self, observer):
        self._observers.append(observer)
    
