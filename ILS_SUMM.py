import numpy as np
import scipy.spatial
from auxiliary_functions import calculate_total_distance
from auxiliary_functions import update_representative_points
from auxiliary_functions import find_best_improvement_normalized_cost

def ILS_SUMM(X, C, budget, ILS_max_trails=1):
    np.random.seed(100)
    distance_mat = scipy.spatial.distance_matrix(X, X)

    # Initialize the representative points:
    if np.min(C) > budget:
        print("The budget is less than the cheapest point!")
        return None
    else:
        curr_representative_points = [np.argmin(C)]

    # Local search for a local minimum:
    best_curr_representative_points, best_curr_total_distance = Local_Search(X, C, budget, initial_representative_points=curr_representative_points, distance_mat=distance_mat)

    # Initialize the best global point:
    best_global_representative_points = best_curr_representative_points
    best_global_total_distance = best_curr_total_distance

    MAX_M = 5
    for k in range(ILS_max_trails):
        M = 1
        while M <= MAX_M:
            # if k%10 == 0:
            print("ILS_SUMM - iteration number: " + str(k))
            print("Total distance: " + str(best_global_total_distance))
            # Perturb the best current point:
            curr_M = int(np.floor(np.min([len(best_curr_representative_points), M, len(C)-len(best_curr_representative_points)])))  # Ensure the size of permutation M is valid.
            exploration_representative_points = perturbation(X, C, budget, best_curr_representative_points, curr_M)
            # Local search for a local minimum, starting from the exploration point:
            best_exploration_representative_points, best_exploration_total_distance = Local_Search(X, C, budget, initial_representative_points=exploration_representative_points, distance_mat=distance_mat)
            # Decide which point will be the next curr point:
            best_curr_representative_points, best_curr_total_distance = acceptance_criterion(best_curr_representative_points, best_curr_total_distance, best_exploration_representative_points, best_exploration_total_distance)
            # Update the best global solution if a better point was found:
            if best_exploration_total_distance < best_global_total_distance:
                M = 1
                best_global_representative_points = best_exploration_representative_points
                best_global_total_distance = best_exploration_total_distance
            else:
                M += 1


    return best_global_representative_points, best_global_total_distance


def Local_Search(X, C, budget, initial_representative_points = None, distance_mat = None, Local_Search_max_trails=1000):
    np.random.seed(100)
    if distance_mat is None:
        distance_mat = scipy.spatial.distance_matrix(X, X)

    # Initialize the representative points:
    if initial_representative_points is not None:
        best_representative_points = initial_representative_points
    else:
        if np.min(C) > budget:
            print("The budget is less than the cheapest point!")
            return None
        else:
            best_representative_points = [np.argmin(C)]

    best_total_distance = calculate_total_distance(distance_mat, best_representative_points)

    for k in range(Local_Search_max_trails):
        if k%10 == 0:
            print("Local Search - iteration number: " + str(k))
            print("Total distance: " + str(best_total_distance))
        best_rep_idx, best_point_idx, best_total_distance, IS_LOCAL_DISTANCE_IMPROVED = find_best_improvement_normalized_cost(X, C, budget, distance_mat, best_representative_points, best_total_distance)
        if IS_LOCAL_DISTANCE_IMPROVED == True:
            best_representative_points = update_representative_points(best_representative_points, best_point_idx,
                                                                    best_rep_idx)
        else:
            return best_representative_points, best_total_distance


    return best_representative_points, best_total_distance

def Restart_SUMM(X, C, budget, vid_duration, ILS_max_trails=1):
    np.random.seed(100)
    distance_mat = scipy.spatial.distance_matrix(X, X)

    # Initialize the representative points:
    if np.min(C) > budget:
        print("The budget is less than the cheapest point!")
        return None
    else:
        curr_representative_points = [np.argmin(C)]

    # Local search for a local minimum:
    best_curr_representative_points, best_curr_total_distance = Local_Search(X, C, budget, initial_representative_points=curr_representative_points, distance_mat=distance_mat)

    # Initialize the best global point:
    best_global_representative_points = best_curr_representative_points
    best_global_total_distance = best_curr_total_distance

    idxs = list(range(len(C)))
    permuted_idxs = list(np.random.permutation(idxs))
    for i in permuted_idxs:
        curr_representative_points = [i]
        if C[curr_representative_points] > budget:
            continue
        # Local search for a local minimum:
        best_curr_representative_points, best_curr_total_distance = Local_Search(X, C, budget,
                                                                                 initial_representative_points=curr_representative_points,
                                                                                 distance_mat=distance_mat)
        if best_curr_total_distance < best_global_total_distance:
            best_global_representative_points = best_curr_representative_points
            best_global_total_distance = best_curr_total_distance

    return best_global_representative_points, best_global_total_distance


def perturbation(X, C, budget, best_curr_representative_points, M):
    print("Perturbation with M = " + str(M))
    points_to_throw = np.argsort(-C[best_curr_representative_points])[0:(M)]

    # Build a list with all not medoids points:
    not_medoids_points = []
    for i in range(X.shape[0]):
        if i in best_curr_representative_points:
            pass
        else:
            not_medoids_points.append(i)
    not_medoids_points = np.array(not_medoids_points)

    # Build an array with the cheapest points.
    points_to_add_indices = np.argsort(C[not_medoids_points])[0:(M)]

    # Build a new solution of representative points by substituting costly points with cheap points.
    new_local_best_representative_points = np.copy(best_curr_representative_points)
    new_local_best_representative_points[points_to_throw] = not_medoids_points[points_to_add_indices]

    # Check that the new solution satisfies the budget condition:
    if np.sum(C[new_local_best_representative_points]) <= budget: # It is not necessary to happen because maybe the cheapest point that currently arn't medoids cost more then the current points.
        print("Perturbation is valid, M = " +str(M))
        local_best_representative_points = np.copy(new_local_best_representative_points)  # update to the new representative points
    else:
        local_best_representative_points = np.copy(best_curr_representative_points)  # stay with the original medoids.

    best_curr_representative_points = local_best_representative_points
    return  best_curr_representative_points




def acceptance_criterion(best_curr_representative_points, best_curr_total_distance, best_exploration_representative_points, best_exploration_total_distance, criterion_type='Better'):
    if criterion_type == 'Better':
        if best_curr_total_distance < best_exploration_total_distance:
            return best_curr_representative_points, best_exploration_total_distance
        else:
            return best_exploration_representative_points, best_exploration_total_distance
    elif criterion_type == 'RW':
        return best_exploration_representative_points, best_exploration_total_distance

    elif criterion_type == 'Metropolis':
        if np.random.binomial(1,0.5) == 1:
            best_exploration_representative_points, best_exploration_total_distance = acceptance_criterion(best_curr_representative_points, best_curr_total_distance,
                                 best_exploration_representative_points, best_exploration_total_distance,
                                 criterion_type='Better')
        else:
            best_exploration_representative_points, best_exploration_total_distance = acceptance_criterion(best_curr_representative_points, best_curr_total_distance,
                                 best_exploration_representative_points, best_exploration_total_distance,
                                 criterion_type='RW')
        return best_exploration_representative_points, best_exploration_total_distance
