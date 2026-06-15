def ask_for_graph():
    """
    UI Interface that asks for edges of the graph the user wants to compute the cover of.
    """
    
    print("\n= = = = = = = = = = = =")
    print("  Vertex Cover Computing")
    print("= = = = = = = = = = = =\n")
    print("Please describe the graph by entering its edges.")
    print("For each edge, enter the name of its two nodes.")
    print("To insert a node that is not linked to any other node, use 'Nan' as the second edge component.")
    print('Type "END" to finish entering edges.')
    print('Example edges: (1,2) (3,2) (4, Nan)\n')

    edges = []
    i = 1
    
    while True:
        print(f"Edge {i}:")

        new_edge = []
        j = 1
        
        while j <= 2:
            node = input(f"  Node {j}: ").strip()
            
            if node == "END":
                if len(edges) == 0:
                    print("Error: You must enter at least one edge!\n")
                    break
                else:
                    return edges
            
            if len(node) == 0:
                print("Error: Node name cannot be empty!")
                continue
            
            if len(node) > 5:
                print("Error: Node name is too long! (max 5 characters)")
                continue
            
            new_edge.append(node)
            j += 1

        if len(new_edge) == 2:
            if tuple(new_edge) in edges:
                print("Error: This edge already exists!\n")
            else:
                edges.append(tuple(new_edge))
                i += 1
        
        print()

def ask_for_display() -> str:
    """
    Asks whether the user wants to display the cover for a graph they manually input (in that case, returns "m"),
    use benchmarking functionalities (in that case, returns "b"), or to test branch and bound scalability (in that case, returns "s").
    """
    inpt = str(input('Would you like to:\n' \
    '- input your own graph and visualize its cover: type "M"\n ' \
    '- Display algorithm benchmarks: type "B"\n' \
    '- Test branch and bound scalability: type "S"\n' \
    'Your answer: '))
    return inpt.lower()
        
def ask_for_graph_families() -> list[str]:
    """
    Asks what graph families the user wants displayed in the algorithm benchmark.
    Graph families are chosen among erdos, bipartite, grid or cycle.
    """
    graph_families = ["erdos", "bipartite", "grid", "cycle"]
    inpt = input("\nChoose what graph families you want to be displayed in the algorithm benchmark among:\n      erdos, bipartite, grid, cycle." \
    "\nThey must be separated by commas and no spaces between them.\nYour input: ").strip().split(sep=",")
    for ele in inpt:
        if ele not in graph_families:
            raise ValueError("Graph families must be among erdos, bipartite, grid and cycle")

    return inpt

def ask_for_bnb_display() -> bool:
    """
    Asks the user whether they want branch and bound algorithm displayed in the metrics that depend on the number of vertices.
    """
    while True:
        inpt = str(input("\nWould you like to display branch and bound algorithm in the plots and metrics that depend on " \
        "the number of vertices? (It will lead to longer running time) [ yes | no ]"))
        if inpt.lower() in ["yes", "y"]:
            return True
        elif inpt.lower() in ["no", "n"]:
            return False
        else:
            print("Answer is invalid! Please try again.")