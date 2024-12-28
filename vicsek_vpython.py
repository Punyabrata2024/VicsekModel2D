import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
N = 100  # Number of birds
v0 = 0.3  # Speed of each bird
R = 0.1  # Interaction radius
r = 0.01  # Separation radius to avoid collision
eta = 0.5  # Noise
L = 1.0  # Scale of the canvas - area of flocking
dt = 0.01  # Time step

# Initialize positions and velocities
positions = np.random.rand(N, 2) * L
angles = np.random.rand(N) * 2 * np.pi
velocities = v0 * np.column_stack((np.cos(angles), np.sin(angles)))

# Calculate normalized order parameter
def calc_order_parameter():
    avg_velocity = np.mean(velocities, axis=0)
    order_parameter = np.linalg.norm(avg_velocity) / v0
    return order_parameter

# Update positions function
def update_positions():
    global positions, velocities
    new_velocities = np.zeros_like(velocities)
    for i in range(N):
        # Find neighbors
        diffs = positions - positions[i]
        dists = np.linalg.norm(diffs, axis=1)
        neighbors = (dists < R) & (dists > 0)
        
        if np.any(neighbors):
            # Average direction of neighbors
            avg_velocity = np.mean(velocities[neighbors], axis=0)
            angle = np.arctan2(avg_velocity[1], avg_velocity[0])
            noise = eta * (np.random.rand() - 0.5)
            new_angle = angle + noise
            new_velocities[i] = v0 * np.array([np.cos(new_angle), np.sin(new_angle)])
        else:
            new_velocities[i] = velocities[i]

    velocities = new_velocities
    positions += velocities * dt

    # Handle boundary conditions
    positions = np.mod(positions, L)

# Animation function
def animate(frame):
    update_positions()
    scat.set_offsets(positions)
    arrows.set_offsets(positions)
    arrows.set_UVC(velocities[:, 0], velocities[:, 1])
    order_param = calc_order_parameter()
    order_text.set_text(f"Order Parameter: {order_param:.2f}")

# Plot setup
fig, ax = plt.subplots()
ax.set_xlim(0, L)
ax.set_ylim(0, L)
scat = ax.scatter(positions[:, 0], positions[:, 1], s=20)
arrows = ax.quiver(positions[:, 0], positions[:, 1], velocities[:, 0], velocities[:, 1], angles='xy', scale_units='xy', scale=0.5)  # Adjust scale to make arrows double the size of particles
order_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=14, verticalalignment='top')

ani = animation.FuncAnimation(fig, animate, frames=200, interval=50)
plt.show()
