

class Expression:

    def __init__(self):
        pass

    def visit(self, visitorObject):
        return visitorObject("TODO: Expression", [])


class SimpleExpression:

    def __init__(self):
        pass

    def visit(self, visitorObject):
        return visitorObject("TODO: SimpleExpression", [])