import numpy as np
import matplotlib.pyplot as plt
from utils.geometry import haversine_distance, RouteCircleIntersect
from utils.world_elements import TimeWorldElements
from config import avgspeed

class CostMatrices:
    def __init__(self, locations):
        self.locations = locations
        self.num = len(locations)
        self.distance = np.zeros((self.num, self.num))
        self.time = np.zeros((self.num, self.num))
        self.safety = np.zeros((self.num, self.num))
        self.offset = 0
        self.scaler = TimeWorldElements(self.locations, self.num)
        self.notifications = []

        for i, loc in enumerate(self.locations):
            for j in range(i+1, self.num):
                
                
                # Setting up the Distance Values
                latj, lonj = self.locations[j]
                d = haversine_distance(loc[0], loc[1], latj, lonj)
                self.distance[i][j] = d
                self.distance[j][i] = d

                self.time[i][j] = d / avgspeed
                self.time[j][i] = d / avgspeed

                # Setting up the Safety Values
                scale = np.random.uniform(-1*self.num, self.num)
                self.safety[i][j] += scale
                self.safety[j][i] += scale
                self.offset = self.safety.min()
                if self.offset < 0:
                    self.safety = np.add(self.safety, -1*self.offset)
                    np.fill_diagonal(self.safety, 0)

                #Scaling Time Values
                for k in range(len(self.scaler)):
                    x1 = self.locations[i][1]
                    y1 = self.locations[i][0]

                    x2 = self.locations[j][1]
                    y2 = self.locations[j][0]

                    a1 = self.scaler[k][2]
                    b1 = self.scaler[k][1]
                    r = self.scaler[k][0]
                    type = self.scaler[k][3]
                    scale = self.scaler[k][4]

                    if (RouteCircleIntersect(x1, y1, x2, y2, a1, b1, r)):
                        if type == 0:
                            self.time[i][j] = self.time[i][j] * scale       #Uphill
                            self.time[j][i] = self.time[j][i] / scale       #Downhill
                        else:
                            self.time[i][j] = self.time[i][j] * scale
                            self.time[j][i] = self.time[j][i] * scale
                
    
    
        # I also add some situations beyond these, for eg. a bridge breaking down, where it gets impossible to get to a certain node from some places
        num_affected = np.random.uniform(0.05, 0.25)
        
        nodes_affected = np.random.randint(0, self.num, int(np.round(num_affected * self.num)))

        
        
        for i in nodes_affected:
            n = np.random.uniform(0.4, 0.8)
            routes_with = np.random.randint(0, self.num, int(np.round(n*self.num)))
            affect = [None] * len(routes_with)
            for j in range(len(routes_with)):
                if (i != routes_with[j]) & (routes_with[j] not in affect):
                    self.time[i][routes_with[j]] = 1e15
                    self.time[routes_with[j]][i] = 1e15
                    #self.distance[i][routes_with[j]] *= 100
                    #self.distance[routes_with[j]][i] *= 100
                    s = f"Node {i} and Node {routes_with[j]} now impossible"
                    self.notifications.append(s)
                    affect.append(routes_with[j])
                    

        random_event = np.random.uniform(0,1)
        if (random_event > 0.90):
            one = np.random.choice(nodes_affected)
            print(f"Major Issue: All routes leading to/from Node {one} now impossible/very difficult ")
            for i in range(self.num):
                if i != one:
                    self.time[i][one] = self.time[i][one] * 1e10
                    self.time[one][i] = self.time[one][i] * 1e10
                    #self.distance[i][one] = self.distance[i][one] * 1e8
                    #self.distance[one][i] = self.distance[one][i] * 1e8

    def PlotTimeEffect(self):
        """ 
        Simple function which plots our Time Affecting Zones over our scatterplot
        
        """
        
        # We need to access global x, y or regenerate them. 
        # In the original code x and y were globals.
        # To modularize properly without changing method signature, I should redefine them here or use self.locations
        x = self.locations[:,1]
        y = self.locations[:,0]
        num = self.num
        latmin, latmax, longmin, longmax = y.min(), y.max(), x.min(), x.max()


        for i in range(len(self.notifications)):
            print(self.notifications[i])

        choice = ["Hill", "Bad Terrain", "Good Terrain", "Bottleneck"]
        plt.scatter(x,y,color = "navy", zorder = 10)
        plt.title("Plot of Locations and Real World Time Distortions in our TSP")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        colour = ["yellow", "orange", "green", "red"]

        added_labels = set()

        scale = self.scaler[:,4]

        for item in self.scaler:
            label = choice[int(item[3])] if choice[int(item[3])] not in added_labels else ""
            if label: added_labels.add(label)
            zone = plt.Circle((item[2],item[1]), item[0], color = colour[int(item[3])], alpha = 0.25 + 0.25*((item[4] - scale.min())/(scale.max() - scale.min())), label=label, zorder = 5)
            plt.gca().add_patch(zone)
        plt.grid()
        
        for i in range(num):
            for j in range(i+1, num):
                plt.plot([x[i], x[j]], [y[i], y[j]], 'gray', alpha=0.15, linewidth=0.5, zorder = 1)

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.xlim(longmin-5, longmax+5)
        plt.ylim(latmin-5, latmax+5)
        plt.axis('equal')
        plt.show()    


            
    def PlotSafetyScale(self):
        """ 
        Simple function which plots our Safety metrics over our scatterplot. Darker colours imply less safe (and so costlier) routes.
        
        """
        x = self.locations[:,1]
        y = self.locations[:,0]
        num = self.num
        latmin, latmax, longmin, longmax = y.min(), y.max(), x.min(), x.max()

        plt.scatter(x,y,color = "navy", zorder = 10)
        plt.title("Plot of Locations and Routes, shaded by safety level (darker is worse)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        plt.grid()
    
        for i in range(num):
            for j in range(i+1, num):
                plt.plot([x[i], x[j]], [y[i], y[j]],
                        color=plt.cm.YlOrRd(
                            (self.safety[i, j] - self.safety.min()) /
                            (self.safety.max() - self.safety.min())
                        ),
                        alpha=0.6, linewidth=1)

        plt.xlim(longmin-5, longmax+5)
        plt.ylim(latmin-5, latmax+5)
        plt.axis('equal')
        plt.show()
