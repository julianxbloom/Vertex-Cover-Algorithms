from algorithms import greedy, LP_relaxation_rounding, branch_and_bound
from create_graph import create_size_n_graph
import networkx as nx
import matplotlib.pyplot as plt

def apply_cover(G: nx.Graph, cover_nodes: list) -> nx.Graph:
    """
    Input: nx.Graph object G, cover of the graph as a list of nodes
    Output: nx.Graph object on which the cover is applied (red nodes, yellow edges)
    """
    
    new_G = G.copy()
    for node in cover_nodes:
        new_G.nodes[node]['color'] = 'red'
        new_G.nodes[node]['size'] = 600
        for edge in new_G.edges.data():
            if edge[0] == node or edge[1] == node:
                edge[2]['color'] = '#dede0d'
                edge[2]['width'] = 3
    return new_G


def visualize_cover(G: nx.Graph) -> None:
    """Displays a visualization of the input graph and its  vertex cover with respect to different algorithms: 
        - greedy
        - relaxation rounding
        - branch-and-bound
    """

    def draw_graph(G: nx.Graph, title: str, ax) -> None:
        """
        Draws the input graph at the axis position given as input and with the input title.
        """

        pos = nx.spring_layout(G, seed=42)

        node_colors = list(nx.get_node_attributes(G, 'color').values())
        node_sizes = list(nx.get_node_attributes(G, 'size').values())
        edge_colors = list(nx.get_edge_attributes(G, 'color').values())
        edge_widths = list(nx.get_edge_attributes(G, 'width').values())
        nx.draw_networkx(
            G, 
            pos=pos,
            ax=ax, 
            node_color=node_colors, 
            node_size=node_sizes,
            edge_color=edge_colors,
            width=edge_widths)
        ax.set_title(title)

    fig, axs = plt.subplots(2, 2, figsize=(13, 7))

    draw_graph(G, title='Original Graph', ax=axs[0, 0])

    greedy_cover = greedy(G)
    G_greedy = apply_cover(G, greedy_cover)
    draw_graph(G_greedy, title='Greedy Cover', ax=axs[0, 1])

    lp_cover = LP_relaxation_rounding(G)[0]
    G_lp = apply_cover(G, lp_cover)
    draw_graph(G_lp, title='LP-Relaxation Rounding Cover', ax=axs[1, 0])

    bnb_cover = branch_and_bound(G)
    G_bnb = apply_cover(G, bnb_cover)
    draw_graph(G_bnb, title='Branch-and-bound Cover', ax=axs[1, 1])

    plt.tight_layout()
    plt.show()


def empirical_ratio_against_n(n_values: list = [i for i in range(1, 500, 50)], type: str = "", fixed_p: float = 0.3, include_bnb: bool = True) -> None:
    """
    Plots the empirical ratio against the values of n (number of vertices of the graph) for each value of n in n_values. 
    To avoid long waiting times, either put low values of n or set include_bnb to False, to exclude branch and bound algorithm.
    """

    graphs = [create_size_n_graph(n, p=fixed_p, type=type, seed=0) for n in n_values]
    N = len(graphs)

    LP_results = [LP_relaxation_rounding(G) for G in graphs]

    LP_empirical_ratio = [len(LP_results[i][0])/LP_results[i][1] for i in range(N)]
    LP_curve = plt.plot(n_values, LP_empirical_ratio, label="LP Relaxation Rounding")
    
    greedy_empirical_ratio = [len(greedy(graphs[i]))/LP_results[i][1] for i in range(N)] #compute empirical ratio for each value of n
    greedy_curve = plt.plot(n_values, greedy_empirical_ratio, label="Greedy")

    if include_bnb:
        BnB_empirical_ratio = [len(branch_and_bound(graphs[i]))/LP_results[i][1] for i in range(N)]
        BnB_curve = plt.plot(n_values, BnB_empirical_ratio, label="Branch and bound")
    
    title = f"Number of vertices against empirical ratio for {type} graphs"
    plt.title(title)
    plt.legend(loc="lower right")
    plt.xlabel("Number of vertices (n)")
    plt.ylabel("Empirical ratio")
    plt.ylim(bottom=0)
    plt.show()

def empirical_ratio_against_p(p_values: list = [i/10 for i in range(0, 10, 1)], type: str = "", fixed_n: int = 20, include_bnb: bool = True) -> None:
    """
    Plots the empirical ratio against the values of p (density of the graph) for each value of p in p_values. 
    """

    if not isinstance(fixed_n, int):
        raise TypeError("fixed_n has to be an integer.")

    graphs = [create_size_n_graph(fixed_n, p, type, seed=0) for p in p_values]
    N = len(graphs)

    LP_results = [LP_relaxation_rounding(G) for G in graphs]

    LP_empirical_ratio = [len(LP_results[i][0])/LP_results[i][1] for i in range(N)]
    LP_curve = plt.plot(p_values, LP_empirical_ratio, label="LP Relaxation Rounding")
    
    greedy_empirical_ratio = [len(greedy(graphs[i]))/LP_results[i][1] for i in range(N)] #compute empirical ratio for each value of n
    greedy_curve = plt.plot(p_values, greedy_empirical_ratio, label="Greedy")

    if include_bnb:
        BnB_empirical_ratio = [len(branch_and_bound(graphs[i]))/LP_results[i][1] for i in range(N)]
        BnB_curve = plt.plot(p_values, BnB_empirical_ratio, label="Branch and bound")
    
    title = f"Graph desity against empirical ratio for {type} graphs"
    plt.title(title)
    plt.legend(loc="lower right")
    plt.xlabel("Graph density (p)")
    plt.ylabel("Empirical ratio")
    plt.ylim(bottom=0)
    plt.show()
