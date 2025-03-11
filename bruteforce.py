import numpy as np
import plotly.graph_objects as go

# Lattice grid size
lattice_size = 20  
step_variation = [-1, 0, 1]  

# Generate a 3D lattice grid
def generate_lattice(size):
    x, y, z = np.meshgrid(np.arange(size), np.arange(size), np.arange(size))
    return np.column_stack([x.ravel(), y.ravel(), z.ravel()])

# Generate a random encryption path (simulating brute force attempts)
def generate_encryption_path(start, steps=50):
    path = [start]
    current = np.array(start)

    for _ in range(steps):
        step = np.random.choice(step_variation, size=3)
        current = (current + step) % lattice_size
        path.append(current.copy())

    return np.array(path)

# Create an animated visualization
def visualize_brute_force_attack(path, lattice_points):
    frames = []
    
    for i in range(1, len(path)):
        frames.append(go.Frame(
            data=[
                go.Scatter3d(
                    x=lattice_points[:, 0], y=lattice_points[:, 1], z=lattice_points[:, 2],
                    mode='markers',
                    marker=dict(size=2.5, color='white', opacity=0.5)  # Keep it always visible
                ),
                go.Scatter3d(
                    x=path[:i, 0], y=path[:i, 1], z=path[:i, 2],
                    mode='lines',
                    line=dict(color='red', width=5)  # Brute-force attack path
                )
            ]
        ))

    layout = go.Layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='black',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))  
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='black',
        showlegend=False,
        updatemenus=[{
            "buttons": [
                {"args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}],
                 "label": "Play",
                 "method": "animate"},
                {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                 "label": "Pause",
                 "method": "animate"}
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }]
    )

    # Create figure with initial data (lattice + empty path)
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=lattice_points[:, 0], y=lattice_points[:, 1], z=lattice_points[:, 2],
                mode='markers',
                marker=dict(size=2.5, color='white', opacity=0.5)
            ),
            go.Scatter3d(
                x=[], y=[], z=[],  # Empty at the start, updates during animation
                mode='lines',
                line=dict(color='red', width=5)
            )
        ],
        layout=layout,
        frames=frames
    )

    fig.show()

# Generate lattice and encryption path
start_point = [lattice_size // 2] * 3
lattice_points = generate_lattice(lattice_size)
encryption_path = generate_encryption_path(start_point, steps=50)

# Visualize the attack animation
visualize_brute_force_attack(encryption_path, lattice_points)
