# matplotlib.use("Agg")
import os

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import numpy as np


def plot_warm_up(disparities):
    x_data = [pair[0] for pair in disparities]
    y_data = [pair[1] for pair in disparities]
    plt.plot(x_data, y_data)
    plt.show()


def main(data, grid):
    data_num_people = np.array([pair[1] for pair in data])
    data_income = np.array([pair[0] for pair in data])
    data_house_price = np.array([pair[2] for pair in data])
    fig, ax = plt.subplots()
    cmap = colors.ListedColormap(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.95'])
    # Salary ranges for coloring squares
    bounds = [-1, 1, 10001, 20001, 30001, 40001, 50001, 75001, 150001, 200001, 300001]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    ani = animation.FuncAnimation(fig, animate, len(data_income), fargs=(data_income, ax, cmap, norm, grid,
                                                                         data_num_people, data_house_price),
                                  interval=200, blit=False)
    ani.save(os.path.join('out', 'chart.mp4'))
    plt.show()


def animate(i, *fargs):
    from main import GRID_ROWS, GRID_COLS
    from grid import Grid
    ax = fargs[1]
    cmap = fargs[2]
    norm = fargs[3]
    grid: Grid = fargs[4]
    data_num_people = fargs[5]
    data_house_price = fargs[6]
    ax.imshow(fargs[0][i], cmap=cmap, norm=norm)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, GRID_COLS, 1))
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(0)
    ax.set_yticks(np.arange(-0.5, GRID_ROWS, 1))
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(0)
    for business in grid.get_businesses():
        r, c = business
        if i == 1:
            ax.scatter([c], [r], marker="D", s=100, color="red", label="Business Centers")
        else:
            ax.scatter([c], [r], marker="D", s=100, color="red")
    for education in grid.get_education_centers():
        r, c = education
        if i == 1:
            ax.scatter([c], [r], marker="*", s=120, color="green", label="Education Centers")
        else:
            ax.scatter([c], [r], marker="*", s=120, color="green")
    for crime in grid.get_crime_centers():
        r, c = crime
        if i == 1:
            ax.scatter([c], [r], marker="X", s=100, color="orange", label="Crime Centers")
        else:
            ax.scatter([c], [r], marker="X", s=100, color="orange")
    for text in ax.texts:
        text.set_visible(False)
    for text in ax.texts:
        text.remove()
    if grid.orientation == "row":
        mark = ">"
    else:
        mark = "^"
    for l, freeway in enumerate(grid.get_freeways()):
        for j, freeway_square in enumerate(freeway):
            r, c = freeway_square
            if i == 1 and l == 0 and j == 0:
                ax.scatter([c - 0.15], [r - 0.15], marker=mark, s=100, color="cyan", label="Freeway Squares")
            else:
                ax.scatter([c - 0.15], [r - 0.15], marker=mark, s=100, color="cyan")
    for row in range(grid.get_num_rows()):
        for column in range(grid.get_num_cols()):
            occ_houses = int(data_num_people[i][row, column])
            ax.text(column+0.15, row-0.15, str(occ_houses), color="yellow", fontsize=8)
    for row in range(grid.get_num_rows()):
        for column in range(grid.get_num_cols()):
            price = data_house_price[i][row, column]/1000.0
            ax.text(column+0.05, row+0.15, str(price), color="purple", fontsize=8)
    l = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
              fancybox=True, shadow=True, ncol=4, fontsize="small")
    plt.show()
    # plt.clf()
