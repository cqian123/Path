import numpy
import path
import Offset_fill
import pyclipper
import matplotlib.pyplot as plt
import obb
import math


def find_offset(parts,Bone_Point,r):
    num = len(parts)
    #轨迹点包不包含中心点的标志位
    flag = 0
    #法向量归一化
    for n in range(num):
        Bone_Point[0:3, n] = Bone_Point[0:3, n] / numpy.sqrt(
            Bone_Point[0, n] * Bone_Point[0, n] + Bone_Point[1, n] * Bone_Point[1, n] + Bone_Point[2, n] * Bone_Point[
                2, n])
    point1_crood = numpy.mat(Bone_Point[0:6,0]).T
    point2_crood = numpy.mat(Bone_Point[0:6,1]).T


    #默认方向
    line_p = numpy.mat([[1, 0, 0, 0, 0, 200]]).T
    plane_vp = numpy.mat([[0, -1, 0, 0, 0, 200]]).T
    #用vector_zy前三位存放z向法向量，后三位存放y向向量，共有num列对应层数
    vector_zy = numpy.zeros((6, num - 1))

    # 存储每一层的两个向量数据
    obb_point = obb.obb(point1_crood, point2_crood, line_p, plane_vp, parts[0])

    vector_zy[0, 0] = Bone_Point[0, 0]
    vector_zy[1, 0] = Bone_Point[1, 0]
    vector_zy[2, 0] = Bone_Point[2, 0]
    vector_zy[3, 0] = obb_point[4, 0]
    vector_zy[4, 0] = obb_point[5, 0]
    vector_zy[5, 0] = obb_point[6, 0]


    #开始剪切
    parts_off = Offset_fill.offset(parts[0].T, point1_crood, point2_crood, r)
    pathpoint_all = [parts_off]
    #向内剪切直到剪切后的矩阵为空
    while 1:
        parts_off = Offset_fill.offset(parts_off[0:3, :].T, point1_crood, point2_crood, r*2)
        # parts_off是8行n列
        if parts_off == []:
            parts_off = Offset_fill.offset(parts[0].T, point1_crood, point2_crood, r)
            if parts_off == []:
                flag = 0
                pathpoint_all.pop()
                break
            else:
                flag = 1
                num1 = len(pathpoint_all)
                finpoint = numpy.r_[Bone_Point[3:6, 0], r]
                break
        else:
            pathpoint_all.append(parts_off)


    num1 = len(pathpoint_all)
    #给所有的点进行排序让其运动轨迹连续
    for i in range(num1 - 1):
        num2 = len(pathpoint_all[i + 1][0])
        min = numpy.sqrt((pathpoint_all[i + 1][0, 0] - pathpoint_all[i][0, 0]) * (
                    pathpoint_all[i + 1][0, 0] - pathpoint_all[i][0, 0])
                         + (pathpoint_all[i + 1][1, 0] - pathpoint_all[i][1, 0]) * (
                                     pathpoint_all[i + 1][1, 0] - pathpoint_all[i][1, 0])
                         + (pathpoint_all[i + 1][2, 0] - pathpoint_all[i][2, 0]) * (
                                     pathpoint_all[i + 1][2, 0] - pathpoint_all[i][2, 0]))
        index = 0
        for j in range(1, num2):
            l = numpy.sqrt((pathpoint_all[i + 1][0, j] - pathpoint_all[i][0, 0]) * (
                        pathpoint_all[i + 1][0, j] - pathpoint_all[i][0, 0])
                           + (pathpoint_all[i + 1][1, j] - pathpoint_all[i][1, 0]) * (
                                       pathpoint_all[i + 1][1, j] - pathpoint_all[i][1, 0])
                           + (pathpoint_all[i + 1][2, j] - pathpoint_all[i][2, 0]) * (
                                       pathpoint_all[i + 1][2, j] - pathpoint_all[i][2, 0]))
            if l < min:
                min = l
                index = j
        temp = numpy.c_[pathpoint_all[i + 1][:, index:num2], pathpoint_all[i + 1][:, 0:index - 1]]
        pathpoint_all[i + 1] = temp

    #最后排序好后把中心点加上去
    if flag == 1:
        pathpoint_all[num1 - 1] = numpy.c_[pathpoint_all[num1 - 1], finpoint[:]]


    #排序后把一层的数据点储存在一起
    pathpoint_final = [pathpoint_all[0]]
    for i in range(1, num1):
        num2 = len(pathpoint_all[i][0])
        for j in range(num2):
            # print(pathpoint_all[i][:,j])
            pathpoint_final[0] = numpy.c_[pathpoint_final[0],pathpoint_all[i][:, j]]

    num2 = len(pathpoint_final[0][0,:])
    point_end = pathpoint_final[0][:,num2-1]
    '''
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.xlabel('x')
    plt.ylabel('y')
    x = pathpoint_final[0][0,:]
    y = pathpoint_final[0][1,:]
    z = pathpoint_final[0][2,:]
    ax.plot3D(x, y, z, 'r-')

    ax.legend()
    plt.show()
    '''

    #切后续的其他层
    for n in range(1, num-1):
        point1_crood = numpy.mat(Bone_Point[0:6, n]).T
        point2_crood = numpy.mat(Bone_Point[0:6, n+1]).T
        parts_off = Offset_fill.offset(parts[n].T, point1_crood, point2_crood, r)
        pathpoint_all.append(parts_off)
        #继续剪切
        while 1:
            parts_off = Offset_fill.offset(parts_off[0:3, :].T, point1_crood, point2_crood, r*2)
            # parts_off是8行n列
            if parts_off == []:
                parts_off = Offset_fill.offset(parts[0].T, point1_crood, point2_crood, r)
                if parts_off == []:
                    flag = 0
                    pathpoint_all.pop()
                    break
                else:
                    flag = 1
                    num1_d = len(pathpoint_all)
                    finpoint = numpy.r_[Bone_Point[3:6, n], r]
                    break
            else:
                pathpoint_all.append(parts_off)


        #偏置完成后计算累计有偏置多少次
        num1_d = len(pathpoint_all)

        # 如果是奇数层先将轨迹变为逆时针，这样倒序后就会变为顺时针
        if n%2==1:
            for i in range(num1, num1_d):
                num_p = len(pathpoint_all[i][0])
                reservedpath = numpy.array(pathpoint_all[i], copy=True)
                for j in range(num_p):
                    pathpoint_all[i][:,j] = reservedpath[:,num_p-1-j]


        # 先使本层第一个点和上一层轨迹连续
        num2 = len(pathpoint_all[num1][0])
        min = numpy.sqrt((pathpoint_all[num1][0, 0] - point_end[0]) * (
                pathpoint_all[num1][0, 0] - point_end[0])
                         + (pathpoint_all[num1][1, 0] - point_end[1]) * (
                                 pathpoint_all[num1][1, 0] - point_end[1])
                         + (pathpoint_all[num1][2, 0] - point_end[2]) * (
                                 pathpoint_all[num1][2, 0] - point_end[2]))
        index = 0
        for j in range(1, num2):
            l = numpy.sqrt((pathpoint_all[num1][0, j] - point_end[0]) * (
                    pathpoint_all[num1][0, j] - point_end[0])
                           + (pathpoint_all[num1][1, j] - point_end[1]) * (
                                   pathpoint_all[num1][1, j] - point_end[1])
                           + (pathpoint_all[num1][2, j] - point_end[2]) * (
                                   pathpoint_all[num1][2, j] - point_end[2]))
            if l < min:
                min = l
                index = j
        temp = numpy.c_[pathpoint_all[num1][:, index:num2], pathpoint_all[num1][:, 0:index - 1]]
        pathpoint_all[num1] = temp

        # 同层点由外向内排序
        for i in range(num1, num1_d - 1):
            num2 = len(pathpoint_all[i + 1][0])
            min = numpy.sqrt((pathpoint_all[i + 1][0, 0] - pathpoint_all[i][0, 0]) * (
                    pathpoint_all[i + 1][0, 0] - pathpoint_all[i][0, 0])
                             + (pathpoint_all[i + 1][1, 0] - pathpoint_all[i][1, 0]) * (
                                     pathpoint_all[i + 1][1, 0] - pathpoint_all[i][1, 0])
                             + (pathpoint_all[i + 1][2, 0] - pathpoint_all[i][2, 0]) * (
                                     pathpoint_all[i + 1][2, 0] - pathpoint_all[i][2, 0]))
            index = 0
            for j in range(1, num2):
                l = numpy.sqrt((pathpoint_all[i + 1][0, j] - pathpoint_all[i][0, 0]) * (
                        pathpoint_all[i + 1][0, j] - pathpoint_all[i][0, 0])
                               + (pathpoint_all[i + 1][1, j] - pathpoint_all[i][1, 0]) * (
                                       pathpoint_all[i + 1][1, j] - pathpoint_all[i][1, 0])
                               + (pathpoint_all[i + 1][2, j] - pathpoint_all[i][2, 0]) * (
                                       pathpoint_all[i + 1][2, j] - pathpoint_all[i][2, 0]))
                if l < min:
                    min = l
                    index = j
            temp = numpy.c_[pathpoint_all[i + 1][:, index:num2], pathpoint_all[i + 1][:, 0:index - 1]]
            pathpoint_all[i + 1] = temp

        #如果标志位为1，则加上中心点
        if flag == 1:
            pathpoint_all[num1_d - 1] = numpy.c_[pathpoint_all[num1_d - 1], finpoint[:]]

        #把排序后的该层的所有点存储在一起
        pathpoint_final.append(pathpoint_all[num1])
        for i in range(num1+1, num1_d):
            num2 = len(pathpoint_all[i][0])
            for j in range(num2):
                # print(pathpoint_all[i][:,j])
                pathpoint_final[n] = numpy.c_[pathpoint_final[n], pathpoint_all[i][:, j]]

        #如果是奇数层就倒序存放
        if n%2==1:
            num_p = len(pathpoint_final[n][0])
            reservedpath = numpy.array(pathpoint_final[n], copy=True)
            for j in range(num_p):
                pathpoint_final[n][:,j] = reservedpath[:,num_p-1-j]


        #计算该层的两个向量并存储
        obb_point = obb.obb(point1_crood, point2_crood, line_p, plane_vp, parts[n])

        vector_zy[0, n] = Bone_Point[0, n]
        vector_zy[1, n] = Bone_Point[1, n]
        vector_zy[2, n] = Bone_Point[2, n]
        vector_zy[3, n] = obb_point[4, 0]
        vector_zy[4, n] = obb_point[5, 0]
        vector_zy[5, n] = obb_point[6, 0]

        #更新迭代参数
        num1 = num1_d
        num2 = len(pathpoint_final[n][0, :])
        point_end = pathpoint_final[n][:, num2 - 1]

        '''
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        plt.xlabel('x')
        plt.ylabel('y')
        x = pathpoint_final[n][0, :]
        y = pathpoint_final[n][1, :]
        z = pathpoint_final[n][2, :]
        ax.plot3D(x, y, z, 'r-')

        ax.legend()
        plt.show()
        '''

    return pathpoint_final,vector_zy