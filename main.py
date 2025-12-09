import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from config import duration, avgspeed
from data.location_generator import get_location_data
from models.cost_matrices import CostMatrices
from solver.tsp_solver import TSPSolver, print_solution

def get_next_example_dir(base_path, num_nodes):
    """
    Determines the next example directory name.
    Pattern: <num_nodes> - Example - <N>
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    
    pattern = os.path.join(base_path, f"{num_nodes} - Example - *")
    existing_dirs = glob.glob(pattern)
    
    max_n = 0
    for d in existing_dirs:
        try:
            # Extract the N part from the folder name
            dirname = os.path.basename(d)
            parts = dirname.split(' - ')
            if len(parts) == 3:
                n = int(parts[2])
                if n > max_n:
                    max_n = n
        except ValueError:
            continue
            
    next_n = max_n + 1
    new_dir_name = f"{num_nodes} - Example - {next_n}"
    full_path = os.path.join(base_path, new_dir_name)
    os.makedirs(full_path)
    return full_path

def plot_route_on_ax(ax, route, locations, title, color_code='blue'):
    """
    Helper function to plot a route on a given matplotlib axis.
    """
    x = locations[:,1]
    y = locations[:,0]
    
    # Plot all nodes
    ax.scatter(x, y, color="navy", zorder=10, s=20)
    
    # Plot the route
    route_x = []
    route_y = []
    for node_idx in route:
        route_x.append(locations[node_idx][1])
        route_y.append(locations[node_idx][0])
    
    # Add lines connecting the route
    ax.plot(route_x, route_y, color=color_code, alpha=0.7, linewidth=1.5, zorder=5)
    
    # Mark start/end
    ax.scatter(route_x[0], route_y[0], color='green', s=50, label='Start', zorder=15)
    ax.scatter(route_x[-1], route_y[-1], color='red', s=50, label='End', zorder=15)
    
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True)

if __name__ == "__main__":
    # Get locations
    location = get_location_data()
    
    # Determine output directory
    num = len(location)
    output_dir = get_next_example_dir("examples", num)
    print(f"Saving outputs to: {output_dir}")

    # Initial Plotting
    s = duration
    sample = num

    x = location[:,1]
    y = location[:,0]

    latmin, latmax, longmin, longmax = y.min(), y.max(), x.min(), x.max()
    
    plt.figure(figsize=(10, 8))
    plt.scatter(x,y, color = "navy", zorder = 10)
    plt.title("Plot of Nodes and All Possible Routes in our TSP")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid()
    plt.xlim(longmin-5, longmax+5)
    plt.ylim(latmin-5, latmax+5)
    for i in range(num):
        for j in range(i+1, num):
            plt.plot([x[i], x[j]], [y[i], y[j]], 'gray', alpha=0.35, linewidth=0.5)
            
    # Save Initial Plot
    plt.savefig(os.path.join(output_dir, "initial_network.png"), bbox_inches='tight')
    plt.close()

    # Create World
    world = CostMatrices(location) #Define the class based on locations

    print("AFFECT ON TIME COSTS DUE TO REAL WORLD ELEMENTS")
    print(f"\nNOTE: In addition, some random effects on time/distance caused by accidents (eg. bridge collapse) are also occuring. If major accident, you will be notified.\n")

    # Save Time Effect Plot
    world.PlotTimeEffect(save_path=os.path.join(output_dir, "time_effect.png"))

    print(f"--------------------------------------------")

    print("AFFECT ON SAEFTY")
    # Save Safety Scale Plot
    world.PlotSafetyScale(save_path=os.path.join(output_dir, "safety_scale.png"))
    print(f"--------------------------------------------")

    # Solve
    mandist, routdist, soldist = TSPSolver(world.distance)
    mantime, routtime, soltime = TSPSolver(world.time)
    mansafe, routsafe, solsafe = TSPSolver(world.safety)

    print("Optimising for Distance (in km):")
    route_d, dist_d, time_d, safety_d = print_solution(mandist, routdist, soldist, world)
    print(f"--------------------------------------------\n\n")

    print("Optimising for Time (in hours, assuming average speed of 50km/hr:")
    route_t, dist_t, time_t, safety_t = print_solution(mantime, routtime, soltime, world)
    print(f"--------------------------------------------\n\n")

    print("Optimising for Safety:")
    route_s, dist_s, time_s, safety_s = print_solution(mansafe, routsafe, solsafe, world)
    print(f"--------------------------------------------\n\n")

    #Creating a Route with custom weights

    distance_weight = 0.3
    time_weight = 0.3
    safety_weight = 0.4

    newmatrix = np.add(np.multiply(distance_weight, world.distance), np.multiply(time_weight, world.time), np.multiply(safety_weight, world.safety))

    manweight, routweight, solweight = TSPSolver(newmatrix)

    print("Optimised for Custom Weights:")
    route_w, dist_w, time_w, safety_w = print_solution(manweight, routweight, solweight, world)
    print(f"--------------------------------------------\n\n")
    
    # Create Collage
    fig, axs = plt.subplots(2, 2, figsize=(20, 16))
    
    # Plot Distance Optimized
    plot_route_on_ax(axs[0, 0], route_d, location, 
                     f"Optimized for Distance\nDist: {dist_d:.1f}km, Time: {time_t:.1f}hr, Safe: {safety_d:.1f}", 
                     color_code='blue')
    
    # Plot Time Optimized
    plot_route_on_ax(axs[0, 1], route_t, location, 
                     f"Optimized for Time\nDist: {dist_t:.1f}km, Time: {time_t:.1f}hr, Safe: {safety_t:.1f}", 
                     color_code='green')
    
    # Plot Safety Optimized
    plot_route_on_ax(axs[1, 0], route_s, location, 
                     f"Optimized for Safety\nDist: {dist_s:.1f}km, Time: {time_s:.1f}hr, Safe: {safety_s:.1f}", 
                     color_code='orange')
    
    # Plot Weighted Optimized
    plot_route_on_ax(axs[1, 1], route_w, location, 
                     f"Optimized for Custom Weights\nDist: {dist_w:.1f}km, Time: {time_w:.1f}hr, Safe: {safety_w:.1f}", 
                     color_code='purple')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "optimisation_collage.png"), bbox_inches='tight')
    plt.close()
    
    print(f"All outputs have been saved to {output_dir}")
