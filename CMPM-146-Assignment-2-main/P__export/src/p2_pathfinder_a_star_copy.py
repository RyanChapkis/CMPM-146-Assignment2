"""
import heapq
import math

def euclidean_dist(current_position, destination):
    x,y = current_position
    a,b = destination
    
    return math.sqrt((x-a)**2 + (y-b)**2)

def find_path (source_point, destination_point, mesh):
    #Mesh is a dictionary with box dimensions and lists of adjacent boxes
    #Source and dest are POINTS! Not boxes!

    #First thing we want to try is returning a list of boxes

    source_box = (0, 0, 0, 0)
    dest_box = (0, 0, 0, 0)
    detail_points = {} #a dictionary the maps boxes to (x,y) pairs.

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
    #previous boxes that have been traversed
    boxes = {}
    path_taken = []

    #the distance traversed thus far
    distance_so_far = {}
    distance_so_far[source_point] = 0

    start_heuristic = euclidean_dist(source_point, destination_point)

    frontier = [(start_heuristic, source_box, source_point)]

    boxes[source_box] = None
    detail_points[source_box] = source_point

    while(len(frontier) > 0):
        priority, current_box, current_point = heapq.heappop(frontier)

        if current_box == dest_box:
            # Insert current_box into boxes, w/ previous as value
            path.append(destination_point)
            while(current_box != None):
                path_taken.append(current_box)
                path.append(detail_points[current_box])
                current_box = boxes[current_box] #destination point should already have something in boxes
            break

        neighbors = mesh['adj'][current_box] #Hopefully this gets the neighbor list?
        for neighbor in neighbors:
            if(neighbor not in boxes):

                xMin, yMin = max(current_box[0], neighbor[0]), max(current_box[2], neighbor[2])
                xMax, yMax = min(current_box[1], neighbor[1]), min(current_box[3], neighbor[3])
                             
                clamp_pointX = max(xMin, min(current_point[0], xMax))
                clamp_pointY = max(yMin, min(current_point[1], yMax))
                neighbor_point = (clamp_pointX, clamp_pointY)

                new_distance = distance_so_far[current_point] + euclidean_dist(current_point, neighbor_point)

                #if new_distance < distance_so_far[neighbor_point]:
                if neighbor not in boxes or new_distance < distance_so_far[neighbor_point]:
                    distance_so_far[neighbor_point] = new_distance
                    priority = new_distance + int(euclidean_dist(neighbor_point, destination_point))

                    boxes[neighbor] = current_box #Add neighbor to list of boxes
                    detail_points[neighbor] = neighbor_point #Add neighbor and its point to point list
                    heapq.heappush(frontier, (priority, neighbor, neighbor_point))

    return path, path_taken #Replaced boxes.keys() w/ path_taken

    """