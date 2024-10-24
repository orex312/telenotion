from db_connection import malke_connection

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Connection(metaclass=Singleton):
    connect = None

    def __init__(self):
        self.connect = malke_connection()
