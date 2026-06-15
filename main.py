from visuals import visualize_cover, empirical_ratio_against_n, empirical_ratio_against_p
from create_graph import create_graph
from UI import ask_for_graph, ask_for_display, ask_for_graph_families, ask_for_bnb_display
from compare import print_metrics, BnB_scalability


def main():
    query = ask_for_display()
    if query == "m":
        # Manual Graph Input
        inpt = ask_for_graph()
        G = create_graph(inpt)
        visualize_cover(G)
        print_metrics(G)

    elif query == "b":
        # Algorithm Benchmarks
        graph_families = ask_for_graph_families()
        include_bnb = ask_for_bnb_display()
        for family in graph_families:
            empirical_ratio_against_p(type=family)
            empirical_ratio_against_n(type=family, include_bnb=include_bnb)

    elif query == "s":
        # Branch and Bound Scalability
        BnB_scalability()

    else:
        print("Invalid answer!")


if __name__ == "__main__":
    main()