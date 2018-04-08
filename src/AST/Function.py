

class Function:

    def __init__(self, name, args, body, returns):
        self.name = name        # string
        self.args = args        # list of Argument nodes
        self.body = body        # list of nodes
        self.returns = returns  # type


class Argument:

    def __init__(self, type, name):
        self.type = type    # Type node
        self.name = name    # string
