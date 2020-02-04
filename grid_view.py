import time

import matplotlib
# matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import numpy as np

def main(data):
    ims = []
    fig, ax = plt.subplots()
    # for i in range(len(data)):
    cmap = colors.ListedColormap(['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9'])
    bounds = [0, 10001, 20001, 30001, 40001, 50001, 60001, 75001, 100001, 300001]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    #     im = ax.imshow(data[-1], cmap=cmap, norm=norm)
    #     ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    #     ax.set_xticks(np.arange(-0.5, 10, 1))
    #     ax.set_yticks(np.arange(-0.5, 10, 1))
    #     plt.show()
    # time.sleep(0.1)
    ani = animation.FuncAnimation(fig, animate, len(data), fargs=(data, ax, cmap, norm), interval=100, blit=False)
    ani.save('chart.mp4')
    plt.show()
    # a=1
    # ani = animation.ArtistAnimation(fig, ims, interval=1, blit=True, repeat_delay=1)
    # plt.show()


def animate(i, *fargs):
    ax = fargs[1]
    cmap = fargs[2]
    norm = fargs[3]
    ax.imshow(fargs[0][i], cmap=cmap, norm=norm)
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-0.5, 10, 1))
    ax.set_yticks(np.arange(-0.5, 10, 1))
    plt.show()
    # return ax

if __name__ == '__main__':
    main(0)