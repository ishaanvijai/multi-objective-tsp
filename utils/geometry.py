import numpy as np

def haversine_distance(lat1, long1, lat2, long2):
    """
    This function takes in two locations (with their latitudes/longitudes separately), and 
    returns the Haversine distance between them, also known as the Great Circle Distance (in km).
    
    """

    earth_radius = 6371
    deltalon = np.radians(long2 - long1)
    deltalat = np.radians(lat2 - lat1)

    a = np.sin(deltalat / 2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(deltalon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return earth_radius*c

def RouteCircleIntersect(x1,y1, x2, y2, a1, b1, r):

    """
    This function takes two nodes' locations as individual entries and a Circle entry in terms of its centre and radius.

    It is a fairly straightfroward function which returns "True" if the route between the two nodes intersects with the circle at any time, "False" if not. 
    
    """
        

    dx = x2 - x1
    dy = y2 - y1

    fx = x1 - a1
    fy = y1 - b1

    a = dx*dx + dy*dy
    b = 2 * (fx*dx + fy*dy)
    c = fx*fx + fy*fy - r*r

    D = b*b - 4*a*c

    if D < 0:
        return False
    
    int1 = (-b + np.sqrt(D)) / (2*a)
    int2 = (-b - np.sqrt(D)) / (2*a)

    return (0<= int1 <= 1) or (0 <= int2 <= 1) or (int1 < 0 and int2 > 1)
