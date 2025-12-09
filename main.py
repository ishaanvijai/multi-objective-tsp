import numpy as np
import matplotlib.pyplot as plt
from config import duration, avgspeed
from data.location_generator import get_location_data
from models.cost_matrices import CostMatrices
from solver.tsp_solver import TSPSolver, print_solution

if __name__ == "__main__":
    # Get locations
    location = get_location_data()
    
    # Initial Plotting
    s = duration
    num = len(location)
    sample = num

    x = location[:,1]
    y = location[:,0]

    latmin, latmax, longmin, longmax = y.min(), y.max(), x.min(), x.max()
    meanlat = y.mean()
    sdlat = y.std()
    meanlong = x.mean()
    sdlong = x.std()


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
            

    plt.show()

    # Create World
    world = CostMatrices(location) #Define the class based on locations

    print("AFFECT ON TIME COSTS DUE TO REAL WORLD ELEMENTS")
    print(f"\nNOTE: In addition, some random effects on time/distance caused by accidents (eg. bridge collapse) are also occuring. If major accident, you will be notified.\n")

    world.PlotTimeEffect()

    print(f"--------------------------------------------")

    print("AFFECT ON SAEFTY")
    world.PlotSafetyScale()
    print(f"--------------------------------------------")

    # Solve
    mandist, routdist, soldist = TSPSolver(world.distance)
    mantime, routtime, soltime = TSPSolver(world.time)
    mansafe, routsafe, solsafe = TSPSolver(world.safety)

    print("Optimising for Distance (in km):")
    print_solution(mandist, routdist, soldist, world)
    print(f"--------------------------------------------\n\n")

    print("Optimising for Time (in hours, assuming average speed of 50km/hr:")
    print_solution(mantime, routtime, soltime, world)
    print(f"--------------------------------------------\n\n")

    print("Optimising for Safety:")
    print_solution(mansafe, routsafe, solsafe, world)
    print(f"--------------------------------------------\n\n")

    #Creating a Route with custom weights

    distance_weight = 0.3
    time_weight = 0.3
    safety_weight = 0.4

    newmatrix = np.add(np.multiply(distance_weight, world.distance), np.multiply(time_weight, world.time), np.multiply(safety_weight, world.safety))

    manweight, routweight, solweight = TSPSolver(newmatrix)

    print("Optimised for Custom Weights:")
    print_solution(manweight, routweight, solweight, world)
    print(f"--------------------------------------------\n\n")
