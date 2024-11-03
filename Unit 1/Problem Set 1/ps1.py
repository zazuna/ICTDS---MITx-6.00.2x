###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
# Recursive Version
def greedy_cow_transport(cows, limit=10, total_transported=[]):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # Base Case Scenario
    if len(cows) == 0:
        return total_transported

    # Transported on this trip
    transported = []

    # Total Weight of Cows on Current Trip
    total_weight = 0

    # Sorting Cows for easier usage
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    for cow in sorted_cows:
        if total_weight + cow[1] <= limit:
            transported.append(cow[0])
            total_weight += cow[1]
            cows.pop(cow[0])

    # Filling up Already Transported Information
    total_transported.append(transported)

    # Calling Transportation Scheme Recursively
    if len(transported) > 0:
        greedy_cow_transport(cows, limit, total_transported)
    return total_transported

# Non-Recursive Version
def greedy_cow_transport2(cows, limit=10):
    transported = []
    total_transported = []
    total_weight = 0
    trips = 0
    while len(cows) != 0:
        sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse=True)
        for cow in sorted_cows:
            if total_weight + cow[1] <= limit:
                transported.append(cow[0])
                total_weight += cow[1]
                cows.pop(cow[0])

        total_transported.append(transported)
        trips += 1
        transported = []
        total_weight = 0

    return total_transported, trips

# Problem 2
def brute_force_cow_transport(cows, limit=10, memo={}):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # for combo in
    result = []
    trips = 0
    for cows_transported in get_partitions(cows):
        trip_count = 0
        grab = True
        for group in cows_transported:
            cargo_weight = 0
            cows_in_cargo = len(group)
            for cow in group:
                if cargo_weight + cows[cow] <= limit:
                    cargo_weight += cows[cow]
                    cows_in_cargo -= 1
            if cows_in_cargo == 0:
                trip_count += 1
            else:
                grab = False
                break

        if grab:
            if trips == 0:
                result = cows_transported
                trips = trip_count
            elif trip_count < trips:
                result = cows_transported

    return result, trips

# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    pass


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
# cows = {'Horns': 50, 'Louis': 45, 'Polaris': 20, 'Muscles': 65, 'Milkshake': 75, 'Patches': 60, 'Clover': 5, 'Miss Bella': 15, 'MooMoo': 85}
# cows = {'Horns': 50, 'Louis': 45, 'Polaris': 20, 'Muscles': 65, 'Milkshake': 75}
# cows = {'Miss Bella': 25, 'Boo': 20, 'MooMoo': 50, 'Lotus': 40, 'Milkshake': 40, 'Horns': 25}
print(cows)


start = time.perf_counter()
# print(greedy_cow_transport(cows, limit))
# print(greedy_cow_transport2(cows, limit))
print(brute_force_cow_transport(cows, limit))
stop = time.perf_counter()
print(stop - start)

