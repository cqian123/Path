import numpy as np
import find_pathpoint
import wfile
import plotpath
import pickle
import find_offset
import Sort_point
import pandas as pd
from scipy.io import loadmat
import math
import translate
import matlab_write
import matlab_write1

r = 0.4

file = loadmat("D:/project/PycharmProjects/new_path/M2_60度16mm弯管/M2_60度16mm弯管/Outlines_0.4.mat")
parts = file['Outlines']

file1 = loadmat("D:/project/PycharmProjects/new_path/M2_60度16mm弯管/M2_60度16mm弯管/Slice_Plane_0.4.mat")
Bone_Point = file1['T_Slice_Plane']

#骨骼点位置调换
Bone_Point[[0,1,2,3,4,5],:] = Bone_Point[[3,4,5,0,1,2],:]

#轮廓点去重复点并用parts_new存放
num = parts.shape[1]
parts_new = [parts[0, 0][:, 0]]
num_n = parts[0, 0].shape[1]
for i in range(1, num_n):
    if (math.fabs(parts[0, 0][0, i - 1] - parts[0, 0][0, i]) < 1e-1) and (
            math.fabs(parts[0, 0][1, i - 1] - parts[0, 0][1, i]) < 1e-1) and (
            math.fabs(parts[0, 0][2, i - 1] - parts[0, 0][2, i]) < 1e-1):
        pass
    else:
        parts_new[0] = np.column_stack((parts_new[0], parts[0, 0][:, i]))
for n in range(1, num):
    num_n = parts[0, n].shape[1]
    parts_new.append(parts[0, n][:,0])
    for i in range(1, num_n):
        if (math.fabs(parts[0,n][0, i-1] - parts[0,n][0, i]) < 1e-2) and (
                math.fabs(parts[0,n][1, i-1] - parts[0,n][1, i]) < 1e-2) and (
                math.fabs(parts[0,n][2, i-1] - parts[0,n][2, i]) < 1e-2):
            pass
        else:
            parts_new[n] = np.column_stack((parts_new[n],parts[0 , n][:, i]))


#pathpoint = find_pathpoint.Parallel_point(parts,Bone_Point,r)
pathpoint_final,vector_zy = find_offset.find_offset(parts_new,Bone_Point,r)
# print(pathpoint)


#plotpath.plotpath(pathpoint_final)
#转换到机械臂运动的坐标系重
#pathpoint_tran = translate.tran(pathpoint_final,Bone_Point,)

#plotpath.plotpath(pathpoint_tran)
#wfile.wrfile(pathpoint_final,pathpoint_tran,vector_zy,"D:/project/PycharmProjects/new_path", "path")

matlab_write.mwrfile(pathpoint_final,pathpoint_final,vector_zy,"D:/project/PycharmProjects/new_path", "feipath")

