import heapq

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

    for box in mesh['boxes']:
        #print(box)
        if source_point[0] >= box[0] and source_point[0] <= box[1]:
            if source_point[1] >= box[2] and source_point[1] <= box[3]:
                source_box = box #This might not get the key

        if destination_point[0] >= box[0] and destination_point[0] <= box[1]:
            if destination_point[1] >= box[2] and destination_point[1] <= box[3]:
                dest_box = box #This might not get the key

    #for box in mesh['adj']:
        #print(box)
        #print(" this a box")

    #The keys for both parts of the mesh are quadruples

    path = []
    boxes = {}
    path_taken = []

    frontier = []
    heapq.heapify(frontier) #Not sure but a different queue type might be better?
    heapq.heappush(frontier, source_box)

    boxes[source_box] = None

    while(len(frontier) > 0):
        current_box = heapq.heappop(frontier)

        if current_box == dest_box:
            # Insert current_box into boxes, w/ previous as value
            while(current_box != None):
                path_taken.append(current_box)
                current_box = boxes[current_box] #destination point should already have something in boxes
            break

        neighbors = mesh['adj'][current_box] #Hopefully this gets the neighbor list?
        for neighbor in neighbors:
            if(neighbor not in boxes):
                boxes[neighbor] = current_box #Add neighbor to list of boxes
                heapq.heappush(frontier, neighbor)

    print(path_taken)
    return path, path_taken #Replaced boxes.keys() w/ path_taken
