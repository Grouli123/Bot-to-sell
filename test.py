from observable import Observable
from observer import Observer


observable2 = Observable()
observer2 = Observer()
observable2.register_observer(observer2)
observable2.value = "Hello, World!"
