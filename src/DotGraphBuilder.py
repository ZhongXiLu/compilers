
from graphviz import Digraph


def DotGraphBuilder(root, children):

    nodes = {}
    idCounter = 0

    graph = Digraph(root)

    # Create root node
    rootId = idCounter
    nodes[rootId] = root
    idCounter += 1
    graph.node(str(rootId), nodes[rootId])

    # Create children
    for child in children:

        if type(child) is str:
            childId = idCounter
            nodes[childId] = child
            idCounter += 1

            graph.node(str(childId), nodes[childId])
            graph.edge(str(rootId), str(childId))

        else:
            graph.subgraph(child)

    return graph
