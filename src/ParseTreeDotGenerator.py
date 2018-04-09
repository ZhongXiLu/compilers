
from graphviz import Digraph


class ParseTreeDotGenerator:

    def __init__(self):
        self.nodes = {}
        self.idCounter = 0

    def generateDOT(self, parser, tree, render=False):
        dot = Digraph("Parse Tree")

        # Create root
        id = self.createIDEntry(parser.ruleNames[tree.getRuleIndex()])
        dot.node(str(id), self.nodes[id])

        self.visit(dot, parser, tree, id)

        dot.render("parse_tree.gv", view=render)

    def createIDEntry(self, value):
        id = self.idCounter
        self.nodes[id] = value
        self.idCounter += 1
        return id

    def visit(self, dot, parser, parseTree, id):

        for child in parseTree.getChildren():

            if child.getChildCount() == 0:  # terminal
                childId = self.createIDEntry(child.getText())
                dot.edge(str(id), str(childId))
                dot.node(str(childId), self.nodes[childId])

            else:
                childId = self.createIDEntry(parser.ruleNames[child.getRuleIndex()])
                dot.edge(str(id), str(childId))
                dot.node(str(childId), self.nodes[childId])
                self.visit(dot, parser, child, childId)
