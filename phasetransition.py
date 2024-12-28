import numpy as np
import matplotlib.pyplot as plt

# Parameters
v0 = 0.3  # Speed of each bird
R = 1  # Interaction radius
r = 0.01  # Separation radius to avoid collision
L = 4.0  # Scale of the canvas - area of flocking
dt = 0.001  # Time step
T = 50  # Simulation time
realizations = 15  # Number of realizations
noise_values = np.linspace(0, 3.5, 10)  # Noise values
N_values = [100, 500, 1000]  # Different values of N

def initialize(N):
    positions = np.random.rand(N, 2) * L
    angles = np.random.rand(N) * 2 * np.pi
    velocities = v0 * np.column_stack((np.cos(angles), np.sin(angles)))
    return positions, velocities

def update_positions(positions, velocities, eta, N):
    diffs = positions[:, np.newaxis, :] - positions[np.newaxis, :, :]
    dists = np.linalg.norm(diffs, axis=2)
    neighbors = (dists < R) & (dists > 0)
    
    avg_velocities = np.dot(neighbors, velocities) / np.sum(neighbors, axis=1)[:, np.newaxis]
    angles = np.arctan2(avg_velocities[:, 1], avg_velocities[:, 0])
    noise = eta * (np.random.rand(N) - 0.5)
    new_angles = angles + noise
    
    velocities = v0 * np.column_stack((np.cos(new_angles), np.sin(new_angles)))
    positions += velocities * dt

    # Handle boundary conditions
    positions = np.mod(positions, L)
    return positions, velocities

def calc_order_parameter(velocities):
    avg_velocity = np.mean(velocities, axis=0)
    order_parameter = np.linalg.norm(avg_velocity) / v0
    return order_parameter

# Run simulations for different N values
plt.figure()
for N in N_values:
    avg_order_parameters = []
    for eta in noise_values:
        order_parameters = []
        for _ in range(realizations):
            positions, velocities = initialize(N)
            for _ in range(int(T / dt)):
                positions, velocities = update_positions(positions, velocities, eta, N)
            order_parameters.append(calc_order_parameter(velocities))
        avg_order_parameters.append(np.mean(order_parameters))

    # Plotting
    plt.plot(noise_values, avg_order_parameters, marker='o', label=f'N = {N}')

plt.xlabel('Noise (η)')
plt.ylabel('Average Normalized Order Parameter')
plt.title('Average Normalized Order Parameter vs Noise')
plt.legend()
plt.grid(True)
plt.show()
