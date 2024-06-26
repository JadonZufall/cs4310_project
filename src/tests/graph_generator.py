from src.obj.graph import Graph
import src.obj.graph as graph
from src.obj.node import Node
import random
import copy

MAX_NODES = 31

def generate_tree_graph(num_nodes: int = random.randrange(0, MAX_NODES), weighted: bool = True, directed: bool = False) -> Graph:
    # Generate a list of new nodes and a list of graphs, each containing one of the nodes
    nodes = [Node(str(x), random.randrange(graph.XMIN, graph.XMAX), random.randrange(graph.YMIN, graph.YMAX)) for x in range(0, num_nodes)]
    graphs = [Graph([nodes[i]]) for i in range(0, num_nodes)]

    # Repeatedly randomly merge two graphs until only one remains
    while len(graphs) != 1:
        # Select two graphs from the list
        g1 = random.choice(graphs)
        graphs.remove(g1)
        g2 = random.choice(graphs)

        # Merge them and connect 2 random nodes between the two graphs
        g2.merge(g1, g2.get_random_node(), g1.get_random_node(), weighted, directed)
    
    graphs[0].reorder_nodes()
    return graphs[0]

def generate_complete_graph(num_nodes: int = random.randrange(0, MAX_NODES), weighted: bool = True, directed: bool = False) -> Graph:
    # Generate a list of new nodes and a single graph containing all of the nodes unconnected
    nodes = [Node(str(x), random.randrange(graph.XMIN, graph.XMAX), random.randrange(graph.YMIN, graph.YMAX)) for x in range(0, num_nodes)]
    g = Graph(nodes)

    # Add an edge between every node in the graph 
    for node1 in nodes:
        for node2 in nodes:
            if node1 is not node2:
                g.add_edge(node1, node2, weighted, True)
    g.reorder_nodes()
    return g

def generate_random_graph(num_nodes: int = random.randrange(0, MAX_NODES), weighted: bool = True, directed: bool = False) -> Graph:
    # Generate a list of new nodes and a list of graphs, each containing one of the nodes
    nodes = [Node(str(x), random.randrange(graph.XMIN, graph.XMAX), random.randrange(graph.YMIN, graph.YMAX)) for x in range(0, num_nodes)]
    graphs = [Graph([nodes[i]]) for i in range(0, num_nodes)]

    # Repeatedly randomly merge two graphs
    while len(graphs) != 1:
        # Merge the two graphs but do not add any edges
        g1 = random.choice(graphs)
        graphs.remove(g1)
        g2 = random.choice(graphs)
        
        # take a random sample of nodes from g2 then merge
        g2_nodes = random.sample(g2.get_nodes(), random.randrange(1, g2.get_num_nodes() + 1))
        g2.merge(g1, None, None, weighted, directed)

       
        # For each selected node
        for g2_node in g2_nodes:
            # Take a random sample of nodes from g2
            g1_nodes = random.sample(g1.get_nodes(), random.randrange(1, g1.get_num_nodes() + 1))
            for g1_node in g1_nodes:
                g2.add_edge(g1_node, g2_node, weighted, directed)

        
    graphs[0].reorder_nodes()
    return graphs[0]

def generate_grid_graph(num_nodes: int):
    nodes = []
    for y in range(num_nodes):
        for x in range(num_nodes):
            nodes.append(Node(str(y*num_nodes + x), x=x, y=y, index=y*num_nodes + x))
            
    graph = Graph(nodes)
    for y in range(num_nodes):
        for x in range(num_nodes):
            node = graph._nodes[y*num_nodes + x]
            if x != 0:
                left = graph._nodes[y*num_nodes + x - 1]
                graph.add_edge(node, left, True, True)
            if x != num_nodes - 1:
                right = graph._nodes[y*num_nodes + x + 1]
                graph.add_edge(node, right, True, True)
            if y != 0:
                above = graph._nodes[(y-1)*num_nodes + x]
                graph.add_edge(node, above, True, True)
            if y != num_nodes - 1:
                below = graph._nodes[(y+1)*num_nodes + x]
                graph.add_edge(node, below, True, True)
    return graph