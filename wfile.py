import numpy as np
import math

def wrfile(pathpoint,pathpoint_t,vector,file_path,file_name):
    file_path_name = file_path + "\\\\" + file_name + ".txt"
    z_vector = np.matrix([[0],[0],[1]])
    vector_n = np.zeros((1,3))
    f = open(file_path_name, 'w')
    l = len(pathpoint_t)
    for n in range(l):
        for i in range(len(pathpoint[n][0])-1):
            if(math.fabs(pathpoint[n][0,i]-pathpoint[n][0,i+1])<1e-3)and(math.fabs(pathpoint[n][1,i]-pathpoint[n][1,i+1])<1e-3)and(math.fabs(pathpoint[n][2,i]-pathpoint[n][2,i+1])<1e-3):
                pass
            else:
                f.writelines("px ")
                f.writelines("%.6f"%(pathpoint_t[n][0,i]*0.001))
                f.writelines(" py ")
                f.writelines("%.6f"%(pathpoint_t[n][1, i]*0.001))
                f.writelines(" pz ")
                f.writelines("%.6f"%(pathpoint_t[n][2, i]*0.001))
                f.writelines(" pv ")
                if i==0:
                    speed = 7.54/(math.pow((pathpoint[n][3, i]),1))
                    f.writelines("%.6f"%(speed*0.001))
                else:
                    speed = 3.77/(math.pow((pathpoint[n][3, i]), 1))
                    f.writelines("%.6f"%(speed*0.001))
                f.writelines('\n')
        if (math.fabs(pathpoint[n][0,len(pathpoint[n][0])-1] - pathpoint[n][0, 0]) < 1e-3) and (
        math.fabs(pathpoint[n][1, len(pathpoint[n][0])-1] - pathpoint[n][1, 0]) < 1e-3) and (
        math.fabs(pathpoint[n][2, len(pathpoint[n][0])-1] - pathpoint[n][2, 0]) < 1e-3):
            pass
        else:
            f.writelines("px ")
            f.writelines("%.6f" % (pathpoint_t[n][0, len(pathpoint_t[n][0])-1] * 0.001))
            f.writelines(" py ")
            f.writelines("%.6f" % (pathpoint_t[n][1, len(pathpoint_t[n][0])-1] * 0.001))
            f.writelines(" pz ")
            f.writelines("%.6f" % (pathpoint_t[n][2, len(pathpoint_t[n][0])-1] * 0.001))
            f.writelines(" pv ")
            speed = 3.77/ (math.pow(pathpoint[n][3, len(pathpoint_t[n][0])-1],1))
            f.writelines("%.6f" % (speed * 0.001))
            f.writelines('\n')


        for i in range(3):
            vector_n[0,i]=vector[i,n]

        #??????????????????
        theta = math.degrees(math.acos(np.dot(vector_n[0, 0:3], z_vector)/(math.sqrt(np.dot(vector_n[0, 0:3],vector_n[0, 0:3].T)))))
        f.writelines("Level %2d theta = %2.3f\n" % (n, theta))

    f.close()
    print("???????????????")

    '''         for j in range(4):
                    f.writelines(str(pathpoint[n][j,i])+', ')'''