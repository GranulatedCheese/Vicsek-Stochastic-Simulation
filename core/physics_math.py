import numpy as np

def initialize_system(num_agents, box_size):
    """
    Generates the init state of mosh pit.
    """
    positions = np.random.uniform(0, box_size, size=(num_agents, 2))
    angles = np.random.uniform(-np.pi, np.pi, size=num_agents)
    return positions, angles

def get_new_angles(positions, angles, radius, noise, box_size):
    """
    Core Vicsek Logic (Vectorized using Linear Algebra)
    """
    num_agents = len(angles)
    
    dx = np.subtract.outer(positions[:, 0], positions[:, 0])
    dy = np.subtract.outer(positions[:, 1], positions[:, 1])
    
    dx = dx - box_size * np.round(dx / box_size)
    dy = dy - box_size * np.round(dy / box_size)
    
    distances = np.sqrt(dx**2 + dy**2)
    
    neighbor_mask = distances < radius
    adjacency_matrix = neighbor_mask.astype(int)
    
    sum_sines = np.dot(adjacency_matrix, np.sin(angles))
    sum_cosines = np.dot(adjacency_matrix, np.cos(angles))
    avg_angles = np.arctan2(sum_sines, sum_cosines)
    
    random_noise = np.random.uniform(-noise/2, noise/2, size=num_agents)
    new_angles = avg_angles + random_noise
    
    return new_angles

def update_positions(positions, angles, velocity, box_size):
    positions[:, 0] += velocity * np.cos(angles)
    positions[:, 1] += velocity * np.sin(angles)
    
    positions = positions % box_size
    
    return positions