
from graphviz import Digraph


def DotGraphBuilder(root, children):

    # Note: graph name is equal to root id
    rootId = DotGraphBuilder.idCounter
    DotGraphBuilder.idCounter += 1
    graph = Digraph(str(rootId))

    # Create root node
    graph.node(str(rootId), root)

    # Create children
    for child in children:

        if type(child) is str:
            childId = DotGraphBuilder.idCounter
            DotGraphBuilder.idCounter += 1

            graph.node(str(childId), child)
            graph.edge(str(rootId), str(childId))

        else:
            graph.subgraph(child)
            graph.edge(str(rootId), str(child.name))

    return graph


DotGraphBuilder.idCounter = 0