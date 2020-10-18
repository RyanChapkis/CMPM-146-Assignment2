from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush
from itertools import product, starmap, islice


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """

    fringe = [(0, initial_position, [initial_position])]       # structure = (cost, position, path to position from start)
    explored = {initial_position: 0}                           # dictionary of explored nodes with keys = position tuple, values = cost
    discovered = {initial_position: 0}

    # While we still have unexplored states that we can visit
    while len(fringe) != 0:
        currentState = heappop(fringe)

        currentCost = currentState[0]   # Breaking up the fringe tuple
        currentPos = currentState[1]
        currentPath = currentState[2]

        # If we have reached our destination, return the path we used to get here
        if currentPos == destination:
            return currentPath

        explored[currentPos] = currentCost  # Dictionary of explored nodes, with nodes as keys and their min cost

        neighbors = adj(graph, currentPos)  # Finding neighbors of the current cell using the adj parameter (always navigation_edges)

        # For each neighbor the adjacency function found
        for neighbor in neighbors:
            neighborPos = neighbor[0]
            neighborCost = int(neighbor[1])     # Just making sure...

            # If we have yet to explore that neighbor, then add it to the fringe as a discovered, unexplored node
            if neighborPos not in explored and neighborPos not in discovered:
                updatedPath = currentPath.copy()    # Updating the neighbor's path in this manner is necessary, otherwise I get an error
                updatedPath.append(neighborPos)
                heappush(fringe, (neighborCost + currentCost, neighborPos, updatedPath))

                discovered[neighborPos] = neighborCost + currentCost

    return None     # Just return None, we shouldn't be getting here if there is a path anyway


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    fringe = [(0, initial_position, [initial_position])]
    shortestPaths = {initial_position: 0}   # Instead of explored nodes, we want the shortest paths to nodes

    while len(fringe) != 0:
        currentState = heappop(fringe)

        currentCost = currentState[0]
        currentPos = currentState[1]
        currentPath = currentState[2]

        neighbors = adj(graph, currentPos)

        for neighbor in neighbors:
            neighborPos = neighbor[0]
            neighborCost = int(neighbor[1])

            # Making this var here since it is more convenient and used in most of the if statements
            pathToNeighborCost = neighborCost + currentCost

            # If we haven't seen this neighbor before, add it to the fringe and to the shortest paths dictionary
            if neighborPos not in shortestPaths:
                updatedPath = currentPath.copy()
                updatedPath.append(neighborPos)
                heappush(fringe, (pathToNeighborCost, neighborPos, updatedPath))

                shortestPaths[neighborPos] = pathToNeighborCost

            # If we have seen this node before, let's do some comparing
            if neighborPos in shortestPaths:

                '''
                If this new path we found is lower cost than a previous path we found,
                update the dictionary and re-add the node to the fringe, since we might
                also find shorter paths to other nodes
                '''
                if pathToNeighborCost < shortestPaths[neighborPos]:
                    shortestPaths[neighborPos] = pathToNeighborCost

                    updatedPath = currentPath.copy()
                    updatedPath.append(neighborPos)
                    heappush(fringe, (pathToNeighborCost, neighborPos, updatedPath))

    return shortestPaths


def navigation_edges(level, cell):
    """
    A reworked navigation_edges function that works the same as current navigation_edges. This function, however, does
    not return costs as chars; instead, it returns them as integers. Furthermore, walls are not present in the list
    returned by this version of the function.
    """
    neighbors = []

    x = cell[0]
    y = cell[1]
    spaces = level['spaces']

    up = (x, y+1)
    down = (x, y-1)
    left = (x-1, y)
    right = (x+1, y)

    up_left = (x-1, y+1)
    up_right = (x+1, y+1)
    down_left = (x-1, y-1)
    down_right = (x+1, y-1)

    if up in spaces:
        neighbors.append((up, spaces[up]))
    if down in spaces:
        neighbors.append((down, spaces[down]))
    if left in spaces:
        neighbors.append((left, spaces[left]))
    if right in spaces:
        neighbors.append((right, spaces[right]))

    if up_left in spaces:
        neighbors.append((up_left, spaces[up_left]))
    if up_right in spaces:
        neighbors.append((up_right, spaces[up_right]))
    if down_left in spaces:
        neighbors.append((down_left, spaces[down_left]))
    if down_right in spaces:
        neighbors.append((down_right, spaces[down_right]))

    return neighbors

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)     # THIS NEEDS TO JUST BE NAVIGATION_EDGES LATER!!!!!
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    print(src)

    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
