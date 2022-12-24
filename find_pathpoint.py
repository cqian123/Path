import numpy
import path
import matplot3
import Offset_fill
import pyclipper
import matplotlib.pyplot as plt

def Parallel_point(parts,Bone_Point,r,rate):
    #parts 是List[list[array[[x,y,z],[x1,y1,z1],  ],array[内圈]],[]]
    #Bon_Point是list[list[array[点],array[法向量]]，list[]]
    #num代表层数
    num = len(parts)
    line_p = numpy.mat([[1, 0, 0, 0, 0, 200]]).T
    plane_vp = numpy.mat([[0, 0, -1, 0, 0, 200]]).T
    for n in range(num):
        Bone_Point[n][1] = Bone_Point[n][1]/numpy.sqrt(Bone_Point[n][1][0]*Bone_Point[n][1][0]+Bone_Point[n][1][1]*Bone_Point[n][1][1]+Bone_Point[n][1][2]*Bone_Point[n][1][2])
    point1_crood = numpy.mat(numpy.r_[Bone_Point[0][1], Bone_Point[0][0]]).T
    point2_crood = numpy.mat(numpy.r_[Bone_Point[1][1], Bone_Point[1][0]]).T
    parts_off = Offset_fill.offset(parts[0][0][0], point1_crood, point2_crood, r)
    # pathpoint_all用list[array[]]来存放所有的点
    pathpoint_all = [parts_off]
    for i in range(4):
        parts_off = Offset_fill.offset(parts_off[3:6,:].T, point1_crood, point2_crood, r)
        # parts_off是8行n列
        pathpoint_all.append(parts_off)
    num1 = len(pathpoint_all)
    # 给所有的点进行排序让其运动轨迹连续
    for i in range(num1 - 1):
        num2 = len(pathpoint_all[i + 1][0])
        min = numpy.sqrt((pathpoint_all[i + 1][3, 0] - pathpoint_all[i][3, 0]) * (
                pathpoint_all[i + 1][3, 0] - pathpoint_all[i][3, 0])
                         + (pathpoint_all[i + 1][4, 0] - pathpoint_all[i][4, 0]) * (
                                 pathpoint_all[i + 1][4, 0] - pathpoint_all[i][4, 0])
                         + (pathpoint_all[i + 1][5, 0] - pathpoint_all[i][5, 0]) * (
                                 pathpoint_all[i + 1][5, 0] - pathpoint_all[i][5, 0]))
        index = 0
        for j in range(1, num2):
            l = numpy.sqrt((pathpoint_all[i + 1][3, j] - pathpoint_all[i][3, 0]) * (
                    pathpoint_all[i + 1][3, j] - pathpoint_all[i][3, 0])
                           + (pathpoint_all[i + 1][4, j] - pathpoint_all[i][4, 0]) * (
                                   pathpoint_all[i + 1][4, j] - pathpoint_all[i][4, 0])
                           + (pathpoint_all[i + 1][5, j] - pathpoint_all[i][5, 0]) * (
                                   pathpoint_all[i + 1][5, j] - pathpoint_all[i][5, 0]))
            if l < min:
                min = l
                index = j
        temp = numpy.c_[pathpoint_all[i + 1][:, index:num2], pathpoint_all[i + 1][:, 0:index - 1]]
        pathpoint_all[i + 1] = temp
    num2 = len(pathpoint_all[num1-1][0])
    pathpoint_all[num1-1][6,num2-1] = 0

    parts_off = Offset_fill.offset(parts_off[3:6, :].T, point1_crood, point2_crood, r)
    pathpoint = path.pathpoint(point1_crood, point2_crood, line_p, plane_vp, parts_off[3:6,:],r)
    pathpoint_all.append(pathpoint[1].getA())
    line = pathpoint[2]
    plane_v = pathpoint[3]

    for n in range(1,num-2):
        point1_crood = numpy.mat(numpy.r_[Bone_Point[n][1],Bone_Point[n][0]]).T
        point2_crood = numpy.mat(numpy.r_[Bone_Point[n+1][1],Bone_Point[n+1][0]]).T
        parts_off = Offset_fill.offset(parts[n][0][0], point1_crood,point2_crood, r)
        pathpoint_all.append(parts_off)
        for i in range(2):
            parts_off = Offset_fill.offset(parts_off[3:6,:].T, point1_crood,point2_crood, r)
            pathpoint_all.append(parts_off)

        num1_d = len(pathpoint_all)
        # 排序
        for i in range(num1, num1_d - 1):
            num2 = len(pathpoint_all[i + 1][0])
            min = numpy.sqrt((pathpoint_all[i + 1][3, 0] - pathpoint_all[i][3, 0]) * (
                    pathpoint_all[i + 1][3, 0] - pathpoint_all[i][3, 0])
                             + (pathpoint_all[i + 1][4, 0] - pathpoint_all[i][4, 0]) * (
                                     pathpoint_all[i + 1][4, 0] - pathpoint_all[i][4, 0])
                             + (pathpoint_all[i + 1][5, 0] - pathpoint_all[i][5, 0]) * (
                                     pathpoint_all[i + 1][5, 0] - pathpoint_all[i][5, 0]))
            index = 0
            for j in range(1, num2):
                l = numpy.sqrt((pathpoint_all[i + 1][3, j] - pathpoint_all[i][3, 0]) * (
                        pathpoint_all[i + 1][3, j] - pathpoint_all[i][3, 0])
                               + (pathpoint_all[i + 1][4, j] - pathpoint_all[i][4, 0]) * (
                                       pathpoint_all[i + 1][4, j] - pathpoint_all[i][4, 0])
                               + (pathpoint_all[i + 1][5, j] - pathpoint_all[i][5, 0]) * (
                                       pathpoint_all[i + 1][5, j] - pathpoint_all[i][5, 0]))
                if l < min:
                    min = l
                    index = j
            temp = numpy.c_[pathpoint_all[i + 1][:, index:num2], pathpoint_all[i + 1][:, 0:index - 1]]
            pathpoint_all[i + 1] = temp

        num2 = len(pathpoint_all[num1_d-1][0])
        pathpoint_all[num1_d-1][6, num2-1] = 0

        parts_off = Offset_fill.offset(parts_off[3:6, :].T, point1_crood, point2_crood, r)
        pathpoint = path.pathpoint(point1_crood, point2_crood, line, plane_v, parts_off[3:6,:],r/rate)
        pathpoint_all.append(pathpoint[1].getA())
        line = pathpoint[2]
        plane_v = pathpoint[3]
        num1_d = len(pathpoint_all)
        num1 = num1_d

    #最后一层
    point1_crood = numpy.mat(numpy.r_[Bone_Point[num-2][1], Bone_Point[num-2][0]]).T
    point2_crood = numpy.mat(numpy.r_[Bone_Point[num-1][1], Bone_Point[num-1][0]]).T
    parts_off = Offset_fill.offset(parts[n][0][0], point1_crood, point2_crood, r)
    pathpoint_all.append(parts_off)
    for i in range(4):
        parts_off = Offset_fill.offset(parts_off[3:6, :].T, point1_crood, point2_crood, r)
        pathpoint_all.append(parts_off)

    num1_d = len(pathpoint_all)
    # 排序
    for i in range(num1, num1_d - 1):
        num2 = len(pathpoint_all[i + 1][0])
        min = numpy.sqrt((pathpoint_all[i + 1][3, 0] - pathpoint_all[i][3, 0]) * (
                pathpoint_all[i + 1][3, 0] - pathpoint_all[i][3, 0])
                         + (pathpoint_all[i + 1][4, 0] - pathpoint_all[i][4, 0]) * (
                                 pathpoint_all[i + 1][4, 0] - pathpoint_all[i][4, 0])
                         + (pathpoint_all[i + 1][5, 0] - pathpoint_all[i][5, 0]) * (
                                 pathpoint_all[i + 1][5, 0] - pathpoint_all[i][5, 0]))
        index = 0
        for j in range(1, num2):
            l = numpy.sqrt((pathpoint_all[i + 1][3, j] - pathpoint_all[i][3, 0]) * (
                    pathpoint_all[i + 1][3, j] - pathpoint_all[i][3, 0])
                           + (pathpoint_all[i + 1][4, j] - pathpoint_all[i][4, 0]) * (
                                   pathpoint_all[i + 1][4, j] - pathpoint_all[i][4, 0])
                           + (pathpoint_all[i + 1][5, j] - pathpoint_all[i][5, 0]) * (
                                   pathpoint_all[i + 1][5, j] - pathpoint_all[i][5, 0]))
            if l < min:
                min = l
                index = j
        temp = numpy.c_[pathpoint_all[i + 1][:, index:num2], pathpoint_all[i + 1][:, 0:index - 1]]
        pathpoint_all[i + 1] = temp

    num2 = len(pathpoint_all[num1_d - 1][0])
    pathpoint_all[num1_d - 1][6, num2 - 1] = 0

    parts_off = Offset_fill.offset(parts_off[3:6, :].T, point1_crood, point2_crood, r)
    pathpoint = path.pathpoint(point1_crood, point2_crood, line, plane_v, parts_off[3:6, :], r)
    pathpoint_all.append(pathpoint[1].getA())



    return pathpoint_all