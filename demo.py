import numpy as np
import os
from ILS_SUMM import ILS_SUMM
import matplotlib.pyplot as plt


SUMM_RATIO = 0.1  # The maximum allowed ratio between the summary video and the full video.

# Load data:
X = np.load(os.path.join('data', 'features.npy'))  # Load n x d feature matrix. n - number of shots, d - feature dimension.
C = np.load(os.path.join('data', 'shots_durations.npy'))  # Load n x 1 shots duration array (number of frames per shot).

# Calculate allowed budget
budget = SUMM_RATIO * np.sum(C)

# Use ILS_SUMM to obtain a representative subset which satisfies the knapsack constraint.
representative_points, total_distance = ILS_SUMM(X, C, budget)
print("The selected shots are" + str(representative_points))
print("The achieved total distance is " +str(total_distance))
# Display Results:
u, s, vh = np.linalg.svd(X)
plt.figure()
point_size = np.divide(C, np.max(C)) * 100
plt.scatter(u[:, 1], u[:, 2], s=point_size, c='lawngreen', marker='o')
plt.scatter(u[representative_points, 1], u[representative_points, 2], s=point_size[representative_points],
            c='blue', marker='o')
plt.title('Solution Visualization (total distance = ' + str(total_distance) + ')')
plt.savefig("Solution_Visualization")
plt.show()


