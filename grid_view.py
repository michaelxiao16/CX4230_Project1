import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import numpy as np

def main(data):
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, animate, frames=1000, interval=100, fargs=(data,))
    plt.show()


def animate(i, *fargs):
    cmap = colors.ListedColormap([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    bounds = [0, 10001, 20001, 30001, 40001, 50001, 60001, 75001, 100001, 300001]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots()
    ax.imshow(*fargs[0][i], cmap=cmap, norm=norm)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, 100, 1))
    ax.set_yticks(np.arange(-0.5, 100, 1))