import heapq

import numpy as np

from config import PERSONAL_SPACE_WEIGHT, PRIVATE_SPACE_WEIGHT
from personal_space import PersonalSpace
from private_space import PrivateSpace


def get_neighborhood(point1, point2, arr):
    x1, y1 = point1
    x2, y2 = point2

    # Find minimum and maximum x and y values
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)

    # Calculate buffer based on distance between points
    buffer = int(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) / 2)

    # Add buffer to each side
    min_x = max(min_x - buffer, 0)
    min_y = max(min_y - buffer, 0)
    max_x = min(max_x + buffer, arr.shape[0] - 1)
    max_y = min(max_y + buffer, arr.shape[1] - 1)

    # Return the subarray
    return arr[min_x:max_x + 1, min_y:max_y + 1], {"min_x": min_x, "min_y": min_y}


def adjacency_matrix_from_image(image, start):
    # get the number of rows and columns in the image
    rows, cols = image.shape
    # create a 2D array of zeroes with the same dimensions as the image
    adj_matrix = np.zeros((rows * cols, rows * cols))
    # iterate through the rows
    for i in range(rows):
        # iterate through the columns
        for j in range(cols):
            # get the index of the current vertex
            current_index = i * cols + j
            # check if there is an edge to the vertex above
            if i > 0:
                if isinstance(image[i - 1][j], PersonalSpace):
                    if image[i - 1][j].position == start:
                        adj_matrix[current_index][current_index - cols] = 1
                    else:
                        adj_matrix[current_index][current_index - cols] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i - 1][j], PrivateSpace):
                    if image[i - 1][j].position == start:
                        adj_matrix[current_index][current_index - cols] = 1
                    else:
                        adj_matrix[current_index][current_index - cols] = PRIVATE_SPACE_WEIGHT
                else:
                    adj_matrix[current_index][current_index - cols] = 1
            # check if there is an edge to the vertex below
            if i < rows - 1:
                if isinstance(image[i + 1][j], PersonalSpace):
                    if image[i + 1][j].position == start:
                        adj_matrix[current_index][current_index + cols] = 1
                    else:
                        adj_matrix[current_index][current_index + cols] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i + 1][j], PrivateSpace):
                    if image[i + 1][j].position == start:
                        adj_matrix[current_index][current_index + cols] = 1
                    else:
                        adj_matrix[current_index][current_index + cols] = PRIVATE_SPACE_WEIGHT
                else:
                    adj_matrix[current_index][current_index + cols] = 1
            # check if there is an edge to the vertex to the left
            if j > 0:
                if isinstance(image[i][j - 1], PersonalSpace):
                    if image[i][j - 1].position == start:
                        adj_matrix[current_index][current_index - 1] = 1
                    else:
                        adj_matrix[current_index][current_index - 1] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i][j - 1], PrivateSpace):
                    if image[i][j - 1].position == start:
                        adj_matrix[current_index][current_index - 1] = 1
                    else:
                        adj_matrix[current_index][current_index - 1] = PRIVATE_SPACE_WEIGHT
                else:
                    adj_matrix[current_index][current_index - 1] = 1
            # check if there is an edge to the vertex to the right
            if j < cols - 1:
                if isinstance(image[i][j + 1], PersonalSpace):
                    if image[i][j + 1].position == start:
                        adj_matrix[current_index][current_index + 1] = 1
                    else:
                        adj_matrix[current_index][current_index + 1] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i][j + 1], PrivateSpace):
                    if image[i][j + 1].position == start:
                        adj_matrix[current_index][current_index + 1] = 1
                    else:
                        adj_matrix[current_index][current_index + 1] = PRIVATE_SPACE_WEIGHT
                else:
                    adj_matrix[current_index][current_index + 1] = 1

            if i > 0 and j < cols - 1:
                if isinstance(image[i - 1][j + 1], PersonalSpace):
                    if image[i - 1][j + 1].position == start:
                        adj_matrix[current_index][current_index - cols + 1] = 1
                    else:
                        adj_matrix[current_index][current_index - cols + 1] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i - 1][j + 1], PrivateSpace):
                    if image[i - 1][j + 1].position == start:
                        adj_matrix[current_index][current_index - cols + 1] = 1
                    else:
                        adj_matrix[current_index][current_index - cols + 1] = PRIVATE_SPACE_WEIGHT
                else:

                    adj_matrix[current_index][current_index - cols + 1] = 1
                # check if there is an edge to the vertex above and to the left
            if i > 0 and j > 0:
                if isinstance(image[i - 1][j - 1], PersonalSpace):
                    if image[i - 1][j - 1].position == start:
                        adj_matrix[current_index][current_index - cols - 1] = 1
                    else:
                        adj_matrix[current_index][current_index - cols - 1] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i - 1][j - 1], PrivateSpace):
                    if image[i - 1][j - 1].position == start:
                        adj_matrix[current_index][current_index - cols - 1] = 1
                    else:
                        adj_matrix[current_index][current_index - cols - 1] = PRIVATE_SPACE_WEIGHT
                else:
                    adj_matrix[current_index][current_index - cols - 1] = 1
                # check if there is an edge to the vertex below and to the right
            if i < rows - 1 and j < cols - 1:
                if isinstance(image[i + 1][j + 1], PersonalSpace):
                    if image[i + 1][j + 1].position == start:
                        adj_matrix[current_index][current_index + cols + 1] = 1
                    else:
                        adj_matrix[current_index][current_index + cols + 1] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i + 1][j + 1], PrivateSpace):
                    if image[i + 1][j + 1].position == start:
                        adj_matrix[current_index][current_index + cols + 1] = 1
                    else:
                        adj_matrix[current_index][current_index + cols + 1] = PRIVATE_SPACE_WEIGHT
                else:
                    adj_matrix[current_index][current_index + cols + 1] = 1
                # check if there is an edge to the vertex below and to the left
            if i < rows - 1 and j > 0:
                if isinstance(image[i + 1][j - 1], PersonalSpace):
                    if image[i + 1][j - 1].position == start:
                        adj_matrix[current_index][current_index + cols - 1] = 1
                    else:
                        adj_matrix[current_index][current_index + cols - 1] = PERSONAL_SPACE_WEIGHT
                elif isinstance(image[i + 1][j - 1], PrivateSpace):
                    if image[i + 1][j - 1].position == start:
                        adj_matrix[current_index][current_index + cols - 1] = 1
                    else:
                        adj_matrix[current_index][current_index + cols - 1] = PRIVATE_SPACE_WEIGHT
                else:
                    adj_matrix[current_index][current_index + cols - 1] = 1
    return adj_matrix


def shortest_path(start_coord, end_coord, initial_board):
    # get the number of rows and columns in the image
    cut_board, mins = get_neighborhood(start_coord, end_coord, initial_board)
    cols = cut_board.shape[1]

    adj_matrix = adjacency_matrix_from_image(cut_board, start_coord)

    start = (start_coord[0] - mins["min_x"]) * cols + start_coord[1] - mins["min_y"]
    end = (end_coord[0] - mins["min_x"]) * cols + end_coord[1] - mins["min_y"]
    # create a dictionary to store the distance from the start vertex for each vertex
    distances = {i: float('inf') for i in range(adj_matrix.shape[0])}
    distances[start] = 0
    heap = [(0, start)]
    previous_vertices = {i: None for i in range(adj_matrix.shape[0] + 1)}
    while heap:
        current_distance, current_vertex = heapq.heappop(heap)
        if current_vertex == end:
            break
        if current_distance == distances[current_vertex]:
            for neighbor in np.nonzero(adj_matrix[current_vertex] > 0)[0]:
                tentative_distance = current_distance + adj_matrix[current_vertex][neighbor]
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(heap, (tentative_distance, neighbor))
    shortest_path = []
    current_vertex = end
    if current_vertex is None:
        return None
    while current_vertex is not None:
        shortest_path.insert(0, current_vertex)

        current_vertex = previous_vertices[current_vertex]
    shortest_path_coord = [index_to_coord(i, cols, mins) for i in
                           shortest_path]  # convert the shortest path from indices to coordinates
    return shortest_path_coord


def index_to_coord(index, cols, mins):
    x, y = index // cols + mins["min_x"], index % cols + mins["min_y"]
    return x, y
