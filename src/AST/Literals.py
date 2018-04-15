

class Number:

    def __init__(self, number):
        self.number = number

    def visit(self, visitorObject):
        return visitorObject(self.number, [])
