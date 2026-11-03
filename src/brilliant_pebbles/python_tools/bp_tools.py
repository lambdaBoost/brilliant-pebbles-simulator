import numpy as np
import math

def bounding_sphere(points):
    """
    Computes an approximate minimum bounding sphere using Ritter's algorithm.
    points: (N, 3) NumPy array of 3D points
    Returns: (center, radius)
    """
    points = np.asarray(points)
    if len(points) == 0:
        return np.zeros(3), 0.0

    # Pick an arbitrary point x
    x = points[0]

    #Find point y furthest from x
    distances_from_x = np.linalg.norm(points - x, axis=1)
    y = points[np.argmax(distances_from_x)]

    #Find point z furthest from y
    distances_from_y = np.linalg.norm(points - y, axis=1)
    z = points[np.argmax(distances_from_y)]

    # Initial sphere diameter is segment [y, z]
    center = (y + z) / 2.0
    radius = np.linalg.norm(y - z) / 2.0
    
    #Expand sphere to include any point outside
    for p in points:
        d = np.linalg.norm(p - center)
        if d > radius:
            radius = (radius + d) / 2.0
            center = center + (d - radius) * (p - center) / d

    return center, radius

def get_intercept_radius(points, intercept_altitude):

    """Calculates the center, radius, and normal vector of the circle of

    intersection between two spheres.

    Parameters:
        c1, c2: tuple/list/array of (x, y, z) for sphere centers
        r1, r2: floats for sphere radii

    Returns:
        dict with 'center', 'radius', and 'normal', or None if no intersection.
    """
    r1 = 6378 + intercept_altitude #earth radius
    c1 = np.array([0,0,0], dtype=float)
    
    c2,r2 = bounding_sphere(points)
    c2 = np.array(c2, dtype=float)

    d_vec = c2 - c1
    d = np.linalg.norm(d_vec)

    # Check for no intersection, containment, or identical centers
    if d > (r1 + r2) or d < abs(r1 - r2) or d == 0:
        return None

    # Distance from center 1 to the plane of the intersection circle
    a = (r1**2 - r2**2 + d**2) / (2 * d)

    # Center point of the intersection circle
    unit_d_vec = d_vec / d
    circle_center = c1 + a * unit_d_vec

    # Radius of the intersection circle
    circle_radius = np.sqrt(max(0.0, r1**2 - a**2))

    # Normal vector of the plane containing the circle
    normal_vector = unit_d_vec

    return {
        'center': circle_center,
        'radius': circle_radius,
        'normal': normal_vector,
    }
    
def get_spacing(radius):
    """_summary_

    Args:
        radius (_type_): _description_
        
    Summary:
    get the spacing between pebbles. Works along orbit and for the distance between orbits
    """
    spacing = (radius*math.sqrt(3))/2
    return spacing

def get_single_orbit_count(spacing):
    """_summary_

    Args:
        spacing (_type_): _description_
    Description:
    number of pebbles in one orbit
    """
    
    earth_circumference = 40075 #oh oh 'Oblate spheroid!!'. Yeah I don't care
    orbit_count = int(earth_circumference/spacing) +1
    return orbit_count

def get_number_or_orbits(inclination, spacing):
    """_summary_

    Args:
        inclination (_type_): _description_
        spacing (_type_): _description_
    Description:
    Number of orbits at a given inclination to achieve global coverage
    Simple calculation - take spacing at equator and apply across a flat projection
    """
    inclination_rad = inclination*(math.pi/180)
    
    #coverage is mininised across equator so we take that as limiting factor
    equitorial_spacing = spacing/(math.sin(inclination_rad))
    
    num_orbits = ((40075/2)/equitorial_spacing)+1
    return num_orbits

def get_min_launch_interval(spacing):
    """_summary_

    Args:
        spacing (_type_): _description_
    Description:
        returns the minimum permissable interval for an icbm launch in a given pebble intercept radius
        applies for a non-redundant cluster
    """
    
    orbital_speed = 7.67 #this is effectivley the same for any interceptor altitude
    return(spacing/orbital_speed)

def get_cluster_requirements(radius, inclination, ssbn_interval):
    """_summary_

    Args:
        radius (_type_): _description_
    Description:
        returns the number of pebbles needed for a nonredundant cluster
    """
    
    spacing = get_spacing(radius)
    single_orbit_count = int(get_single_orbit_count(spacing))
    number_of_orbits = int(get_number_or_orbits(inclination, spacing))
    total_pebbles = single_orbit_count * number_of_orbits
    min_launch_interval = int(get_min_launch_interval(spacing))
    ssbn_margin = min_launch_interval/ssbn_interval  #this is our margin for ssbn defense. <1 means we cannot defend against an ssbn salvo
    
    cluster_results = {'pebble_spacing': spacing,
                       'single_orbit_count': single_orbit_count,
                       'number_of_orbits': number_of_orbits,
                       'total_pebbles': total_pebbles,
                       'min_launch_interval': min_launch_interval,
                       'ssbn_margin': ssbn_margin}
    
    return(cluster_results)