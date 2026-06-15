from algorithms import greedy, LP_relaxation_rounding, branch_and_bound
from create_graph import create_size_n_graph
import time

def compute_metrics(G, algorithm, optimum=None) -> tuple[float, float]:
    """
    Takes as input a networkx.Graph object, an algorithm among the ones implemented (greedy, LP relaxation rounding, branch and bound) 
    and an optimum (lower bound for the cover of the graph, if not provided LP lower bound is used).
    Returns the empirical ratio (length of the cover returned by the algorithm / optimum) and the runtime of the algorithm.
    """

    start = time.time()
    result = algorithm(G)
    end = time.time()
    runtime = end - start

    if isinstance(result, tuple):
        cover, lp_lower_bound = result
        cover_size = len(cover)
        denominator = optimum if optimum is not None else lp_lower_bound
    else:
        cover = result
        cover_size = len(cover)
        denominator = optimum if optimum is not None else LP_relaxation_rounding(G)[1]

    try:
        empirical_ratio = cover_size / denominator
    except ZeroDivisionError:
        raise ZeroDivisionError("Optimum must be a real number different from zero.")

    return empirical_ratio, runtime

def print_alg_metrics(G, algorithm, optimum=None) -> None:
    """
    Prints metrics (empirical ratio and runtime) about an algorithm with respect to a specific graph in the terminal.
    """
    
    empirical_ratio, runtime = compute_metrics(G, algorithm, optimum)

    print(f"\n      {algorithm.__name__}\n")
    print(f"Empirical ratio: {empirical_ratio:.2f}")
    print(f"Runtime: {runtime:.6f}\n")
    print("-----------------------------------------------------------------------")

def print_metrics(G, optimum=None) -> None:
    """
    Prints metrics (empirial ratio and runtime) of greedy, LP relaxation rounding and branch and bound algorithms 
    with respect to the graph given as input.
    """

    print("\n=======================================================================")
    print(f"                           Algorithm Metrics")
    print("=======================================================================\n")

    algorithms = [greedy, LP_relaxation_rounding, branch_and_bound]
    for algorithm in algorithms:
        print_alg_metrics(G, algorithm, optimum)


def BnB_scalability(n_values: list = [10, 20, 50, 100, 200]) -> bool:
    """
    Given a list of values, repeatedly creates size n graphs and computes their branch and bound cover until either all values 
    of the list have been processed or the program raises a timeout or recursion error. 
    Returns False in case recursion or timeout errors are raised, True otherwise.
    The sake of this function is to measure the scalability of the branch and bound algorithm on the size of the graph.
    """

    for n in n_values:
        G = create_size_n_graph(n)
        try:
            print(f"\nCurrently running branch and bound for n = {n}")
            cover = branch_and_bound(G, timeout=5)
            print(f"Found the exact solution for n = {n}!")
        except RecursionError as e:
            print("     " + str(e))
            print(f"Max recursion depth reached at n = {n}\n")
            return False
        except TimeoutError as e:
            print("     " + str(e))
            print(f"Timeout error at n = {n}\n")
            return False
    return True
