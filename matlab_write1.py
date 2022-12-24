import numpy as np
import math

def mwrfile(pathpoint,pathpoint_t,vector,file_path,file_name):
    file_path_name = file_path + "\\\\" + file_name + ".txt"
    z_vector = np.matrix([[0],[0],[1]])
    vector_n = np.zeros((1,3))
    f = open(file_path_name, 'w')
    l = len(pathpoint_t)
    for n in range(4,5):
        for i in range(len(pathpoint[n][0])):
            pathpoint[n][3,i] = np.abs(
        pathpoint_t[n][0, i]  + pathpoint_t[n][2, i]* 62.5 - 5-(10-0.24*4)*62.5-0.24*62.5) / np.sqrt(62.5*62.5 + 1)

        for i in range(len(pathpoint[n][0])-1):
            if(math.fabs(pathpoint[n][0,i]-pathpoint[n][0,i+1])<1e-3)and(math.fabs(pathpoint[n][1,i]-pathpoint[n][1,i+1])<1e-3)and(math.fabs(pathpoint[n][2,i]-pathpoint[n][2,i+1])<1e-3):
                pass
            else:
                f.writelines("%.6f "%(pathpoint_t[n][0, i]))
                f.writelines("%.6f "%(pathpoint_t[n][1, i]))
                f.writelines("%.6f "%(pathpoint_t[n][2, i]))
                f.writelines("%.6f" % (pathpoint[n][3, i]))
                f.writelines('\n')
        if (math.fabs(pathpoint[n][0,len(pathpoint[n][0])-1] - pathpoint[n][0, 0]) < 1e-3) and (
        math.fabs(pathpoint[n][1, len(pathpoint[n][0])-1] - pathpoint[n][1, 0]) < 1e-3) and (
        math.fabs(pathpoint[n][2, len(pathpoint[n][0])-1] - pathpoint[n][2, 0]) < 1e-3):
            pass
        else:
            f.writelines("%.6f " % (pathpoint_t[n][0, len(pathpoint_t[n][0])-1]))
            f.writelines("%.6f " % (pathpoint_t[n][1, len(pathpoint_t[n][0])-1]))
            f.writelines("%.6f " % (pathpoint_t[n][2, len(pathpoint_t[n][0])-1]))
            f.writelines("%.6f" % (pathpoint[n][3, len(pathpoint_t[n][0])-1]))
            f.writelines('\n')

        '''
        for i in range(3):
            vector_n[0,i]=vector[i,n]

        #计算旋转角度
        theta = math.degrees(math.acos(np.dot(vector_n[0, 0:3], z_vector)/(math.sqrt(np.dot(vector_n[0, 0:3],vector_n[0, 0:3].T)))))
        f.writelines("Level %2d theta = %2.3f\n" % (n, theta))
        '''
    f.close()
    print("文件已生成")