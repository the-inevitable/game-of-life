"""
The Conway’s Game of Life has four rules.
"""

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as plt_animation

ON = 255
OFF = 0
values = [ON, OFF]


def random_grid(N):
    """
    Returns a grid of N*N random values.
    More OFF than ON.
    """
    return np.random.choice(values, N*N, p=[0.2, 0.8]).reshape(N, N)


def add_glider(i, j, _grid):
    """
    Adds a glider with top left cell at (i,j).
    """
    glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
    _grid[i:i+3, j:j+3] = glider


def update(frame_num, img, grid, N):
    new_grid = grid.copy()
    for i in range(N):
        for j in range(N):
            # Compute 8-neighbor sum using toroidal boundary conditions
            # x and y wrap around so that the simulation
            # takes place on a toroidal surface without edges.
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N]
                         + grid[(i-1)%N, j] + grid[(i+1)%N, j]
                         + grid[(i-1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]
                         + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])
                        / 255)
            # Apply Conway's rules.
            if grid[i, j] == ON:
                if total < 2 or total > 3:
                    new_grid[i, j] = OFF
            else:
                if total == 3:
                    new_grid[i, j] = ON

    # Update data.
    img.set_data(new_grid)
    grid[:] = new_grid
    return img


# main() function.
def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")
    # Add arguments.
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    args = parser.parse_args()

    # Set grid size.
    N = int(args.N) if args.N and int(args.N) > 8 else 100

    # Set animation update interval.
    update_interval = int(args.interval) if args.interval else 50

    # Declare grid.
    grid = np.array([])

    # Check if "glider" demo flag is specified.
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        add_glider(1, 1, grid)
    else:
        # Populate grid with random on/off - more off than on.
        grid = random_grid(N)

    # Set up the animation.
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    animation = plt_animation.FuncAnimation(
        fig,
        update,
        fargs=(img, grid, N, ),
        frames=60,
        interval=update_interval,
        save_count=50
    )

    # Set the output file.
    if args.movfile:
        movwriter = plt_animation.PillowWriter(fps=30, extra_args=['-vcodec', 'libx264'])
        animation.save(args.movfile, writer=movwriter)

    plt.show()


if __name__ == '__main__':
    main()
