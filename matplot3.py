'''实现plot3的功能'''
import numpy as np
import matplotlib.pyplot as plt

def matplot3(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plt.xlabel('x')
    plt.ylabel('y')
    ax.plot(x, y, z, 'r-', label='Curve', )
    ax.legend()
    plt.show()


'''import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 10
#设置坐标大小，但是只有x,y坐标，而且坐标轴会根据坐标值自动进行调整

fig = plt.figure()
ax = fig.gca(projection='3d')#设置成3维图

plt.xlabel('ai')
plt.ylabel('bi') #设置坐标轴的标号

x = np.random.randint(0,10,20) # 生成20个随机整数
y = np.random.randint(0,10,20)
z = x/(x+y)
ax.plot(x, y, z, 'ro-', label='Curve', )
#label='Curve',curve是曲线但是没看到有什么用

ax.legend()

plt.show()'''