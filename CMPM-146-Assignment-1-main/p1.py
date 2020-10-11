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
    explored = {initial_position: 0}                           # dictionary of explored nodes with positions as the keys

    while len(fringe) != 0:
        currentState = heappop(fringe)
        currentCost = currentState[0]
        currentPos = currentState[1]
        currentPath = currentState[2]
        neighbors = adj(graph, currentPos)

        if currentPos is destination:
            return currentPath

        for neighbor in neighbors:
            neighborPos = neighbor[0]
            neighborCost = int(neighbor[1])

            if neighborPos in explored:
                if neighborCost < explored[currentPos]:
                    explored[currentPos] = neighborCost + currentCost
                if neighborCost >= explored[currentPos]:
                    neighborCost += explored[currentPos]

            currentPath.append(neightborPos)
            heappush(fringe, (neighborCost, neighborPos, currentPath))

    return None


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    pass


def merge(list1, list2): 
    """ Merges the list of all neighboring cells, and their corresponding costs

    Args: 
        list1: list of neigbor cells
        list2: list of costs
    """  
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))] 
    return merged_list 


def level_to_list(level):
    """ converts level to a 2d list/grid that is easier to navigate and augment.

    Args:
        level: The level to be converted to a list.
    """
    xs, ys = zip(*(list(level['spaces'].keys()) + list(level['walls'])))
    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)

    chars = []
    inverted_waypoints = {point: char for char, point in level['waypoints'].items()}

    for j in range(y_lo, y_hi + 1):
        for i in range(x_lo, x_hi + 1):

            cell = (i, j)
            if cell in level['walls']:
                chars.append('X')
            elif cell in inverted_waypoints:
                chars.append(inverted_waypoints[cell])
            elif cell in level['spaces']:
                chars.append(str(int(level['spaces'][cell])))
            else:
                continue
        chars.append('\n')

    str1 = ""
    str_to_list = str1.join(chars)
    
    rows = str_to_list.split()

    return_list = [[c for c in line.strip()] for line in rows]
    
    return(return_list)


def findNeighbors(grid, x, y):
    """ Helper function that returns all the neighbors around a given cell in a grid as well as the neighbor's 
    respective costs.

    Args:
        grid: A 2D list constructed from the level provided in navigation_edges
        x: the x position of the cell provided in navigation_edges
        y: the y position of the cell provided in navigation_edges

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.
    """
    costs = []
    neighbors = []
    if 0 < x < len(grid) - 1:
        xi = (0, -1, 1)   # this isn't first or last row, so we can look above and below
    elif x > 0:
        xi = (0, -1)      # this is the last row, so we can only look above
    else:
        xi = (0, 1)       # this is the first row, so we can only look below
    # the following line accomplishes the same thing as the above code but for columns
    if 0 < y < len(grid[0]) - 1:
        yi = (0, -1, 1)
    elif y > 0:
        yi = (0, -1)
    else:
        yi = (0, 1)
    for a in xi:
        for b in yi:
            if a == b == 0: 
                continue
            costs.append(grid[x+a][y+b])
            neighbors.append((y+b, x+a))
    merged_tuples = merge(neighbors, costs)
    return(merged_tuples)


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    new_level = level_to_list(level)
    x,y = cell
    return(findNeighbors(new_level, x, y))


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
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
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
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')
