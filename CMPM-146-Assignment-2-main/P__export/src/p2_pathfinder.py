import heapq
import math

def euclidean_dist(current_position, destination):
    x,y = current_position
    a,b = destination
    
    return math.sqrt((x-a)**2 + (y-b)**2)

def find_path (source_point, destination_point, mesh):
    #Mesh is a dictionary with box dimensions and lists of adjacent boxes
    #Source and dest are POINTS! Not boxes!

    """
    Searches for a path from source_point to destination_point through the mesh
    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to
    Returns:
        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """

    #First thing we want to try is returning a list of boxes

    """
    Pseudocode
    Scan through the boxes in mesh to find source_box and dest_box
    for each box in mesh:
        if source_point(x) is between top and bottom right x
            if source_point(y) is between top and bottom right y
                source_box = this box
    create a priority queue, push source_point
    create a dictionary came_from containing previous locations
    while priority queue is not empty:
        current_box = queue.pop
        if current_box = destination
            create list path_taken
            using came_from, starting at the desintation, 
                add boxes to path_taken
            return path_taken
        
        for each neighbor of current_box (using mesh)
            (There are no distances so we don't have to worry about that rn)
            if neighbor is not in came_from:
                came_from.append(neighbor)
                queue.push(neighbor)
    
    (did not find a path)
    return None
    """

    source_box = (0, 0, 0, 0)
    dest_box = (0, 0, 0, 0)
    forward_points = {} #a dictionary the maps boxes to (x,y) pairs.
    backward_points = {}

    """
    How to do point to point:
    - start w/ source point in first box
    - take current point and constrain it within the bounds of next box
    """

    #Find the boxes that source and destination are in
    for box in mesh['boxes']:
        if source_point[0] >= box[0] and source_point[0] <= box[1]:
            if source_point[1] >= box[2] and source_point[1] <= box[3]:
                source_box = box #This might not get the key

        if destination_point[0] >= box[0] and destination_point[0] <= box[1]:
            if destination_point[1] >= box[2] and destination_point[1] <= box[3]:
                dest_box = box #This might not get the key

    #The keys for both parts of the mesh are quadruples

    path = []
    path_taken = []

    #the distance traversed thus far
    forward_dist = {}
    forward_dist[source_point] = 0
    backward_dist = {}
    backward_dist[destination_point] = 0

    forward_points[source_box] = source_point
    backward_points[dest_box] = destination_point

    start_heuristic = euclidean_dist(source_point, destination_point)
    #Forth item is the goal
    frontier = [(start_heuristic, source_box, source_point, 'destination')]
    heapq.heappush(frontier, (start_heuristic, dest_box, destination_point, 'start'))

    #previous boxes that have been traversed
    boxes = {}
    boxes[source_box] = None

    #dictionary that stores forward backpointers
    forward_prev = {}
    forward_prev[source_box] = None

    #dictionary that stores backward backpointers
    backward_prev = {}
    backward_prev[dest_box] = None

    while(len(frontier) > 0):
        priority, current_box, current_point, point_of_interest = heapq.heappop(frontier)

        #Forward: Check if current is in the previously traversed backward space
        if point_of_interest == 'destination' and current_box in backward_prev:
            # Insert current_box into boxes, w/ previous as value
            clone = backward_prev[current_box]
            while current_box is not None:
                path_taken.append(current_box)
                path.append(forward_points[current_box])
                current_box = forward_prev[current_box] #destination point should already have something in boxes
            while clone is not None:
                path_taken.insert(0, clone)
                path.insert(0, backward_points[clone])
                clone = backward_prev[clone]
            break
        #Backward: Check if current is in the previously traversed forward space
        elif point_of_interest == 'start' and current_box in forward_prev:
            # Insert current_box into boxes, w/ previous as value
            clone = forward_prev[current_box]
            while current_box is not None:
                path_taken.append(current_box)
                path.append(backward_points[current_box])
                current_box = backward_prev[current_box] #destination point should already have something in boxes
            while clone is not None:
                path_taken.insert(0, clone)
                path.insert(0, forward_points[clone])
                clone = forward_prev[clone]
            break

        try: 
            neighbors = mesh['adj'][current_box] #Hopefully this gets the neighbor list?
            for neighbor in neighbors:
                if point_of_interest == 'destination' and neighbor not in forward_prev:

                    """
                    Take current point and constrain it within the range of the current neighbors
                        rangeX = currentBox(x1 - x2) * neighborbox(x1 - x2)
                        rangeY = currentBox(y1 - y2) * neighborBox(y1 - y2)
                        neighborPoint = current_point
                        constrain(neighborPoint.x, rangeX)
                        constrain(neighborPoint.y, rangeY)
                    """
                    xMin, yMin = max(current_box[0], neighbor[0]), max(current_box[2], neighbor[2])
                    xMax, yMax = min(current_box[1], neighbor[1]), min(current_box[3], neighbor[3])
                                
                    clamp_pointX = max(xMin, min(current_point[0], xMax))
                    clamp_pointY = max(yMin, min(current_point[1], yMax))
                    neighbor_point = (clamp_pointX, clamp_pointY)

                    new_distance = forward_dist[current_point] + euclidean_dist(current_point, neighbor_point)
                    
                    #if new_distance < distance_so_far[neighbor_point]:
                    if neighbor not in forward_prev or new_distance < forward_dist[neighbor_point]:
                        forward_dist[neighbor_point] = new_distance
                        priority = new_distance + int(euclidean_dist(neighbor_point, destination_point))

                        forward_prev[neighbor] = current_box #Add neighbor to list of boxes
                        forward_points[neighbor] = neighbor_point #Add neighbor and its point to point list
                        heapq.heappush(frontier, (priority, neighbor, neighbor_point, 'destination'))
                elif point_of_interest == 'start' and neighbor not in backward_prev:

                    xMin, yMin = max(current_box[0], neighbor[0]), max(current_box[2], neighbor[2])
                    xMax, yMax = min(current_box[1], neighbor[1]), min(current_box[3], neighbor[3])
                                
                    clamp_pointX = max(xMin, min(current_point[0], xMax))
                    clamp_pointY = max(yMin, min(current_point[1], yMax))
                    neighbor_point = (clamp_pointX, clamp_pointY)

                    new_distance = backward_dist[current_point] + euclidean_dist(current_point, neighbor_point)
                    
                    #if new_distance < distance_so_far[neighbor_point]:
                    if neighbor not in backward_prev or new_distance < backward_prev[neighbor_point]:
                        backward_dist[neighbor_point] = new_distance
                        priority = new_distance + int(euclidean_dist(neighbor_point, source_point))

                        backward_prev[neighbor] = current_box #Add neighbor to list of boxes
                        backward_points[neighbor] = neighbor_point #Add neighbor and its point to point list
                        heapq.heappush(frontier, (priority, neighbor, neighbor_point, 'start'))
        except KeyError:
            print('No Path!')

    return path, path_taken #Replaced boxes.keys() w/ path_taken