__author__ = '\"Teardrop\" Ducky'


class Player:
    firstName = None
    lastName = None
    id = None
    value = None
    transferlist = None
    evaluation = None
    position = None
    leg = None
    stats = {}

    def __init__(self, firstName, lastName, id ):
        self.firstName = firstName
        self.lastName = lastName
        self.id = id