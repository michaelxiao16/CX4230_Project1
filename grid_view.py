# matplotlib.use("Agg")
import os

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import numpy as np


def main(data, grid):
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.95'])
    # Salary ranges for coloring squares
    bounds = [-1, 1, 10001, 20001, 30001, 40001, 50001, 75001, 150001, 200001, 300001]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    ani = animation.FuncAnimation(fig, animate, len(data), fargs=(data, ax, cmap, norm, grid), interval=100, blit=False)
    ani.save(os.path.join('out', 'chart.mp4'))
    plt.show()


def animate(i, *fargs):
    from main import GRID_ROWS, GRID_COLS
    ax = fargs[1]
    cmap = fargs[2]
    norm = fargs[3]
    grid = fargs[4]
    ax.imshow(fargs[0][i], cmap=cmap, norm=norm)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, GRID_COLS, 1))
    ax.set_yticks(np.arange(-0.5, GRID_ROWS, 1))
    for business in grid.get_businesses():
        r, c = business
        ax.plot([r], [c], marker="s", markersize=2, color="red")
    for education in grid.get_education_centers():
        r, c = education
        ax.plot([r], [c], marker="s", markersize=2, color="green")
    for row in range(grid.get_num_rows()):
        for column in range(grid.get_num_cols()):
            grid_square = grid.get_grid_square(row, column)
            occ_houses = grid_square.get_occupied_houses()
            ax.text(row+0.15, column-0.15, str(occ_houses), color="yellow", fontsize=8)


    plt.show()
