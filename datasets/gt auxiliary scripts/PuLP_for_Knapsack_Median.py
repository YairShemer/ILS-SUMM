import pulp
import scipy
def PuLP_for_Knapsack_Median(X, C, budget):
    distance_mat = scipy.spatial.distance_matrix(X, X)
    castomers = list(range(X.shape[0]))
    facility = list(range(X.shape[0]))

    # set problem variable
    prob = pulp.LpProblem("FacilityLocation", pulp.LpMinimize)

    # Decision Variables
    serv_vars = pulp.LpVariable.dicts("Service", [(i,j) for i in castomers
                                                        for j in facility], 0, 1, pulp.LpBinary)
    use_vars = pulp.LpVariable.dicts("UseLocation", facility, 0, 1, pulp.LpBinary)

    # objective function
    prob += pulp.lpSum(distance_mat[i,j]*serv_vars[(i,j)] for j in facility for i in castomers)

    # constraints
    for i in castomers:
        prob += pulp.lpSum(serv_vars[(i,j)] for j in facility) == 1

    for i in castomers:
        for j in facility:
            prob += serv_vars[(i,j)] <= use_vars[j]

    prob += pulp.lpSum(C[j]*use_vars[j] for j in facility) <= budget

    # solve
    solve_status = prob.solve()
    print("Status:", pulp.LpStatus[prob.status])
    assert(solve_status == 1)  # See explanation here: https://pythonhosted.org/PuLP/constants.html

    best_representative_points = []
    for i in facility:
        if use_vars[i].varValue > 0.00001:
            best_representative_points.append(i)
    best_total_distance = pulp.value(prob.objective)

    return best_representative_points, best_total_distance