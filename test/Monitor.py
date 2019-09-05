import numpy as np 
from load_sina import LoadNet
import matplotlib.pyplot as plt

if __name__ == '__main__':
    plt.axis([0, 100, 0, 1])
    plt.ion()

    xs = [0, 0]
    ys = [1, 1]

    for i in range(100):
        y = np.random.random()
        xs[0] = xs[1]
        ys[0] = ys[1]
        xs[1] = i
        ys[1] = y
        plt.plot(xs, ys)
        plt.pause(0.1)

