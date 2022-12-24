import numpy as np

point = np.zeros([3,90])
for i in range(90):
    point[0,i] = i-44
    point[2,i] = 0.5+(0.9-0.5)*i/90

file_path_name = "D:/project/PycharmProjects/new_path"+ "\\\\" + "path_line" + ".txt"
f = open(file_path_name, 'w')
for i in range(90):
    f.writelines("px ")
    if point[0,i]>=0:
        f.writelines("%.6f" % (point[0,i] * 0.001))
    else:
        f.writelines("%.5f" % (point[0, i] * 0.001))
    f.writelines(" py ")
    if point[1, i] >= 0:
        f.writelines("%.6f" % (point[1,i] * 0.001))
    else:
        f.writelines("%.5f" % (point[1, i] * 0.001))
    f.writelines(" pz ")
    f.writelines("%.6f" % (point[2,i] * 0.001))
    f.writelines(" pv ")
    #线宽0.8，喷头直径0.4，挤出速度30mm/s
    speed = 0.8*17.18/point[2,i]
    f.writelines("%.6f" % (speed * 0.001))
    f.writelines('\n')

f.writelines("Level %2d theta = %2.3f\n" % (0, 0))
f.close()
print("文件已生成")



