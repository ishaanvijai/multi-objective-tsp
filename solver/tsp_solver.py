from ortools.constraint_solver import routing_enums_pb2 
from ortools.constraint_solver import pywrapcp
import numpy as np
from config import duration

s = duration

def TSPSolver(matrix):
    """
    This function is adapted from Google OR Tools. 

    It solves the TSP. Since we use real world elements, we use a first solution and improvement heuristic which can handle the assymetry of our matrices well.

    First Solution - Parallel Cheapest Insertion

    Improvement - Guided Local Search. 

    NOTE  - We only run the improvement for S seconds, as seen in the first code block
    
    """
    manager = pywrapcp.RoutingIndexManager(len(matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        i = manager.IndexToNode(from_index)
        j = manager.IndexToNode(to_index)
        return int(matrix[i][j])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

    )

    #routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES

    # search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION

    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.FromSeconds(s)
    search_parameters.log_search = False

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    return manager, routing, solution

def print_solution(manager, routing, solution, world):
    """
    This function is adapted from Google OR Tools. 

    It takes in outputs from the TSPSolver and prints out the route, and its "cost" across the three domains of Distance, Time and Safety.
    
    """
    index = routing.Start(0)
    plan_output = "Route:\n"
    route_distance = 0
    route_time = 0
    route_safety = 0
    route = []
    
    while not routing.IsEnd(index):
        node_index = manager.IndexToNode(index)
        route.append(node_index)
        plan_output += f" {node_index} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        
        # Get the actual node indices for matrix lookup
        from_node = manager.IndexToNode(previous_index)
        to_node = manager.IndexToNode(index)
        
        # Calculate costs on all three matrices
        route_distance += world.distance[from_node][to_node]
        route_time += world.time[from_node][to_node]
        route_safety += world.safety[from_node][to_node]
    
    # Add the final node
    final_node = manager.IndexToNode(index)
    route.append(final_node)
    plan_output += f" {final_node}\n"
    plan_output += f"Distance: {np.round(route_distance, 2)} km\n"
    plan_output += f"Time: {np.round(route_time,2)} hr\n" 
    plan_output += f"Safety: {np.round(route_safety,2)}\n"
    
    print(plan_output)
    return route, route_distance, route_time, route_safety
