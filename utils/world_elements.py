import numpy as np

def TimeWorldElements(locations, num):
    """
    This function takes in the locations array, and the number of locations.

    We use this function to add real world elements to our simulation. 

    In particular, we use probability distibutions to add several different situations:

    1 - Hills - These increase time in one direction, and reduce time in another
    2 - Bad Terrain - This increases time along a certain route
    3 - Good Terrain - This reduces time along a certain route
    4 - Bottleneck - This increases time along a certain route, much more than the other elements.

    Further, these are randomly scattered across the region. Each zone is a circle, to ease with our computation. 

    Notably, we allow circles to overlap - this makes our simulation even more engaging. For eg, a route which goes through good and bad terrain may
    be simulating a situation where the raod quality is very good (so time reduces) but it is narrow (so time increases). 


    After creating these zones, we also show a plot of how this compares to our network. Then we scale our time matrix per route based on if it intersects with 
    any of these zones.


    """
    x = locations[:,1]
    y = locations[:,0]

    latmin, latmax, longmin, longmax = y.min(), y.max(), x.min(), x.max()

    if num <= 50:
        var = 0.4
    elif num <= 100:
        var = 0.2
    else:
        var = 0.1
    NumberofZones = int(np.round(4 + 5 * np.log10(num)))   #Number of Zones = n^0.7 to n^0.9
    gridx = np.linspace(longmin, longmax, num*1000)
    gridy = np.linspace(latmin, latmax, num*1000)

    timezones = np.ndarray((NumberofZones, 5))
    radius = np.abs(np.random.uniform((latmax-latmin)*0.05, (latmax-latmin)*0.25, NumberofZones))


    latloc = np.random.uniform(gridy.min(),gridy.max(),NumberofZones)
    longloc = np.random.uniform(gridx.min(),gridx.max(),NumberofZones)
    type = np.random.choice(4, NumberofZones, p=[0.3, 0.3, 0.25, 0.15])
    scale = np.ndarray(NumberofZones)
    for i in range(NumberofZones):
        if type[i] == 0:
            scale[i] = np.random.uniform(1.25,1.75)
        elif type[i] == 1:
            scale[i] = np.random.uniform(1.1,1.5)
        elif type[i] == 2:
            scale[i] = np.random.uniform(0.5,0.9)
        elif type[i] == 3:
            scale[i] = np.random.uniform(1.8,3)

    timezones[:,0] = radius
    timezones[:,1] = latloc
    timezones[:,2] = longloc
    timezones[:,3] = type
    timezones[:,4] = scale

    return timezones
