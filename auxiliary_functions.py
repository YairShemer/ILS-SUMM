import numpy as np


def calculate_total_distance(distance_mat, representative_points):
    effective_distance_mat = distance_mat[:,representative_points]
    distance_to_nearest_neighbor = np.min(effective_distance_mat,1)
    total_distance = np.sum(distance_to_nearest_neighbor)
    return total_distance


def update_representative_points(local_best_representative_points, best_point_idx, best_rep_idx):
    if best_rep_idx == None:
        current_k = local_best_representative_points.__len__()
        temp_local_best_representative_points = np.zeros(current_k + 1, dtype=int)
        temp_local_best_representative_points[:current_k] = local_best_representative_points
        temp_local_best_representative_points[current_k] = best_point_idx
        local_best_representative_points = np.copy(temp_local_best_representative_points)
    else:
        local_best_representative_points[int(np.where(local_best_representative_points == best_rep_idx)[0])] = best_point_idx
    return local_best_representative_points


def find_best_improvement_normalized_cost(X, C, budget, distance_mat, curr_representative_points, curr_total_distance):
    IS_LOCAL_DISTANCE_IMPROVED = False
    best_rep_idx = None
    best_point_idx = None
    curr_representative_points = np.array(curr_representative_points)
    near_points_data = get_near_points_data(distance_mat, curr_representative_points)
    local_best_total_distance = np.copy(curr_total_distance)
    # improvement_counter = 0

    for point_idx in range(X.shape[0]):
        if point_idx in curr_representative_points:
            continue
        if ((np.sum(C[curr_representative_points]) + C[point_idx]) <= budget):
            is_normalized_delta = False
            if is_normalized_delta == False:
                rep_idx = None # Don't replace a medoid but add one.
                delta_swap = get_delta_swap(distance_mat, near_points_data, rep_idx, point_idx)
                temp_total_distance = curr_total_distance + delta_swap
                if temp_total_distance < local_best_total_distance:
                    local_best_total_distance = temp_total_distance
                    best_rep_idx = rep_idx
                    best_point_idx = point_idx
                    IS_LOCAL_DISTANCE_IMPROVED = True
            else:
                best_normalized_delta_swap = 0
                rep_idx = None # Don't replace a medoid but add one.
                delta_swap = get_delta_swap(distance_mat, near_points_data, rep_idx, point_idx)
                delta_cost = C[point_idx]
                normalized_delta_swap = delta_swap / delta_cost
                if normalized_delta_swap < best_normalized_delta_swap:
                    temp_total_distance = curr_total_distance + delta_swap
                    local_best_total_distance = temp_total_distance
                    best_rep_idx = rep_idx
                    best_point_idx = point_idx
                    IS_LOCAL_DISTANCE_IMPROVED = True

    if IS_LOCAL_DISTANCE_IMPROVED == True:
        return best_rep_idx, best_point_idx, local_best_total_distance, IS_LOCAL_DISTANCE_IMPROVED
    else:
        for point_idx in range(X.shape[0]):
            if point_idx in curr_representative_points:
                continue
            for rep_idx in curr_representative_points:
                if (np.sum(C[curr_representative_points]) + C[point_idx] - C[rep_idx]) > budget:
                    continue
                delta_swap = get_delta_swap(distance_mat, near_points_data, rep_idx, point_idx, curr_representative_points)
                temp_total_distance = curr_total_distance + delta_swap
                if temp_total_distance < local_best_total_distance:
                    # If swapping the points decreases the total distance more then other options we checked:
                    # Keep it:
                    local_best_total_distance = temp_total_distance
                    best_rep_idx = rep_idx
                    best_point_idx = point_idx
                    IS_LOCAL_DISTANCE_IMPROVED = True
    return best_rep_idx, best_point_idx, local_best_total_distance, IS_LOCAL_DISTANCE_IMPROVED


def get_near_points_data(distance_mat, representative_points):
    # This function finds the nearest points to each point from the current representative points
    num_of_points = distance_mat.shape[0]
    points_idxs_list = range(num_of_points)
    near_points_data = np.zeros((num_of_points, 3))
    NEAREST_DIST = 0
    NEAREST_IDX = 1
    SECOND_DIST = 2
    # SECOND_IDX = 3
    argsorted_distance_to_rep_points = representative_points[np.argsort(distance_mat[:, representative_points], 1)]
    near_points_data[:, NEAREST_DIST] = distance_mat[tuple(points_idxs_list), tuple(argsorted_distance_to_rep_points[:,0])]
    near_points_data[:, NEAREST_IDX] = argsorted_distance_to_rep_points[:,0]
    if argsorted_distance_to_rep_points.shape[1] > 1:
        near_points_data[:, SECOND_DIST] = distance_mat[tuple(points_idxs_list), tuple(argsorted_distance_to_rep_points[:,1])]
    else:
        near_points_data[:, SECOND_DIST] = np.inf # No second nearest point
        # near_points_data[:, SECOND_IDX] = argsorted_distance_to_rep_points[:,1]
    return near_points_data


def get_delta_swap(distance_mat, near_points_data, original_med, candidate_median, curr_representative_points=None):
    NEAREST_DIST = 0
    NEAREST_IDX = 1
    SECOND_DIST = 2
    SECOND_IDX = 3
    num_of_points = near_points_data.shape[0]
    # points_idxs_list = range(num_of_points)
    delta_tot_dist = 0
    if original_med is None:
        delta_array = distance_mat[:, candidate_median] - near_points_data[:, NEAREST_DIST]
        delta_array_only_negetive = np.divide(delta_array - np.abs(delta_array), 2)
        delta_tot_dist = np.sum(delta_array_only_negetive)
    else:
        auxilary_mat = np.zeros((num_of_points,2))
        auxilary_mat[:, 0] = distance_mat[:, candidate_median] - near_points_data[:, NEAREST_DIST]  # d_oj - d_n
        auxilary_mat[:, 1] = near_points_data[:, SECOND_DIST] - near_points_data[:, NEAREST_DIST]  # d_s - d_n
        original_med_not_nearer_idxs = np.where(~(near_points_data[:, NEAREST_IDX] == original_med))
        auxilary_mat[original_med_not_nearer_idxs, 1] = 0
        delta_tot_dist = np.sum(np.min(auxilary_mat, 1))
    return delta_tot_dist