

class Number:

    def __init__(self, number):
        self.number = number

    def visit(self, visitorObject):
        return visitorObject(self.number, [])


class String:

    def __init__(self, string):
        self.string = string

    def visit(self, visitorObject):
        return visitorObject(self.string, [])