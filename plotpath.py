import numpy as np
import matplotlib.pyplot as plt


def plotpath(pathpoint):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.xlabel('x')
    plt.ylabel('y')
    num = len(pathpoint)
    for i in range(num-1):
        x = pathpoint[i][0, :]
        y = pathpoint[i][1, :]
        z = pathpoint[i][2, :]
        ax.plot3D(x, y, z, 'r-')
        #用于画层与层之间的连线
        x = np.column_stack((pathpoint[i][0, len(pathpoint[i])-1], pathpoint[i + 1][0, 0]))[0]
        y = np.column_stack((pathpoint[i][1, len(pathpoint[i]) - 1], pathpoint[i + 1][1, 0]))[0]
        z = np.column_stack((pathpoint[i][2, len(pathpoint[i]) - 1], pathpoint[i + 1][2, 0]))[0]
        ax.plot3D(x, y, z, 'r-')

    #最后一层
    x = pathpoint[num-1][0, :]
    y = pathpoint[num-1][1, :]
    z = pathpoint[num-1][2, :]
    ax.plot3D(x, y, z, 'r-')

    ax.legend()
    plt.show()