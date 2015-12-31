__author__ = '\"Teardrop\" Ducky'


class Employee:
    firstName = None
    lastName = None
    id = None
    value = None
    age = None
    position = None
    stats = {}

    def __init__(self, id ):
        self.id = id