import itertools 
def tsp_brute_force(graph):
    # Generate all possible permutations of nodes
    nodes = list(graph.nodes)
    permutations = itertools.permutations(nodes)

    # Initialize variables for the best tour and its cost
    best_tour = None
    best_cost = float('inf')

    # Iterate through all permutations and calculate their costs
    for permutation in permutations:
        tour = list(permutation)
        tour.append(tour[0])  # Add the starting node at the end to complete the tour
        cost = 0

        # Calculate the cost of the current tour
        for i in range(len(tour) - 1):
            current_node = tour[i]
            next_node = tour[i + 1]
            if graph.has_edge(current_node, next_node):
                cost += graph[current_node][next_node]['weight']
            else:
                # If there is no direct edge, consider it as an invalid tour
                cost = float('inf')
                break
        #print(permutation,cost)  ////////////////////////////////////////////////////////ACA VEMOS TODOS LOS CASOS
        # Update the best tour and its cost if the current tour is better
        if cost < best_cost:
            best_tour = tour
            best_cost = cost

    return best_tour, best_cost