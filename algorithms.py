import networkx as nx
import pulp
import time

def greedy(G: nx.Graph) -> set:
    """
    Implementation of a greedy algorithm that computes a non-optimal vertex cover of G.
    """

    cover = set()
    edges = set(G.edges)

    while len(edges) > 0:
        u, v = edges.pop()
        cover.add(u)
        cover.add(v)
        edges = {e for e in edges if u not in e and v not in e}
    return cover


def LP_relaxation_rounding(G: nx.Graph) -> tuple[set, float]:
    """
    Implementation of a LP-relaxation rounding algorithm that solves vertex cover problem with the help of pulp library.
    """

    if len(G.edges) == 0:
        return set(), float('inf')
    
    problem = pulp.LpProblem("LP_solver", pulp.LpMinimize)

    # Definition of variables
    x = pulp.LpVariable.dicts("x", G.nodes, lowBound=0, upBound=1)
    problem += pulp.lpSum(x[i] for i in G.nodes)

    # Definition of constraints
    for u, v in G.edges:
        problem += (x[u] + x[v] >= 1)

    # Solving problem using pulp's LP solver
    problem.solve(pulp.PULP_CBC_CMD(msg=False))
    solution = {node: pulp.value(x[node]) for node in G.nodes}

    # Rounding solution
    rounded_cover = set(node for node in G.nodes if solution[node] >= 0.5)

    # Used to compute empirical ratio, not related to cover computing
    lp_lower_bound = pulp.value(problem.objective) 

    return rounded_cover, lp_lower_bound


def branch_and_bound(G: nx.Graph, timeout: float = 60) -> set:
    """
    Implementation of a recursive brand-and-bound algorithm that solves the vertex cover problem.
    By default, timeout raises after running for 60 seconds, if not over.
    """

    start_time = time.time()

    best_cover = set(G.nodes)
    edges = list(G.edges)

    def recursive_branch_and_bound(uncovered_edges: list, current_cover: set) -> set:
        nonlocal best_cover

        # Handles long running time
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Execution exceeded {timeout} seconds.")

        if len(current_cover) >= len(best_cover):
            return
        
        if len(uncovered_edges) == 0:
            best_cover = current_cover.copy()
            return

        u,v = uncovered_edges[0]

        uncovered_edges_u = [e for e in uncovered_edges if u not in e]
        recursive_branch_and_bound(uncovered_edges_u, current_cover | {u})

        uncovered_edges_v = [e for e in uncovered_edges if v not in e]
        recursive_branch_and_bound(uncovered_edges_v, current_cover | {v})

    recursive_branch_and_bound(uncovered_edges=edges, current_cover=set())

    return best_cover
