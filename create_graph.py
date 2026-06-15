import networkx as nx
from math import isqrt, ceil

def get_nodes(input_edges: list) -> list:
    """
    Input: list of tuples of the form (a,b), where (a,b) is an edge of the graph
    Output: list of the nodes of the graph
    """

    nodes = []
    for edge in input_edges:
        if edge[0] not in nodes and edge[0] != "Nan":
            nodes.append((edge[0], {'color': 'grey', 'size': 300}))
        if edge[1] not in nodes and edge[1] != "Nan":
            nodes.append((edge[1], {'color': 'grey', 'size': 300}))
    return nodes

def get_edges(input_edges) -> list:
    """
    Input: list of tuples of the form (a,b), where (a,b) is an edge of the graph
    Output: list of the edges of the graph
    """

    edges = []
    for edge in input_edges:
        if edge[0] != "Nan" and edge[1] != "Nan":
            new_edge = (edge[0], edge[1], {'color': 'black', 'width': 2})
            edges.append(new_edge)
    return edges

def create_graph(input_edges) -> nx.Graph:
    """
    Creates a nx.Graph object from a list of edges
    """

    for ele in input_edges:
        if input_edges.count(ele) > 1:
            raise Exception("All edges must be unique")
        if type(ele) is not tuple:
            raise Exception("All arguments have to be tuples of the form (a, b)")

    nodes = get_nodes(input_edges)
    edges = get_edges(input_edges)

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def create_size_n_graph(n: int, p: float = 0.3, type: str = "", seed: int | None = None) -> nx.Graph:
    """
    Generates a random nx.Graph object with n vertices and a density of p.
    
    Type must be either: "", "erdos", "bipartite", "grid" or "cycle".
    """
    
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    if p < 0 or p > 1:
        raise ValueError("p must be between 0 and 1")

    if not isinstance(type, str):
        raise ValueError("type must be a string")
    type = type.lower()
    if type not in ["", "erdos", "bipartite", "grid", "cycle"]:
        raise ValueError("Type must be either Erdos, Bipartite, Grid or Cycle.")


    if type == "bipartite":
        n1 = n // 2
        n2 = n - n1
        G = nx.bipartite.random_graph(n1, n2, p, seed)
    elif type == "grid":
        rows = isqrt(n)
        cols = ceil(n / rows)
        G = nx.grid_2d_graph(rows,cols)
    elif type == "cycle":
        G = nx.cycle_graph(n)
    else: #handles erdos graphs generation
        G = nx.gnp_random_graph(n, p, seed=seed)

    for node in G.nodes:
        G.nodes[node].update({'color': 'grey', 'size': 300})

    for u, v in G.edges:
        G.edges[u, v].update({'color': 'black', 'width': 2})

    return G
