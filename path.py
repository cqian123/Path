import numpy
import pyclipper
import conversion
import intersects
import thick
import LimitValue
import matplotlib
import limitpoint


def pathpoint(point1_crood, point2_crood, line_p, plane_vp, parts,r):
    parts = numpy.mat(parts)
    plane_c = conversion.conversion(point1_crood[:, 0])
    plane_c = numpy.c_[plane_c,conversion.conversion(point2_crood[:, 0])]
    point_number = parts.shape[1]
    #print(plane_c,point_number)

    if numpy.all(numpy.dot(point1_crood[0:3, 0].T,point2_crood[0:3, 0]) >= 0.99):  # 与后一个平面平行
        line = line_p[0:6, 0]
        plane_v = plane_vp[0:6, 0]
    else:  # 交线存在
        # print(point1_crood,point1_crood[0:3, 0],point1_crood[0:3, 0].T,point2_crood)
        line = numpy.cross(point1_crood[0:3, 0].T, point2_crood[0:3, 0].T)
        # print(line)
        plane_v = numpy.cross(line[0, 0:3], point1_crood[0:3, 0].T)  # 垂直于point1_crood且过直线line(:,1)的平面

        z = (plane_c[1, 0] * plane_c[3, 1] - plane_c[1, 1] * plane_c[3, 0]) / (
                    plane_c[2, 0] * plane_c[1, 1] - plane_c[2, 1] * plane_c[1, 0])
        y = (plane_c[2, 0] * plane_c[3, 1] - plane_c[3, 0] * plane_c[2, 1]) / (
                    plane_c[2, 1] * plane_c[1, 0] - plane_c[2, 0] * plane_c[1, 1])
        rextra = numpy.mat([[0, y, z]]).T
        plane_v = numpy.r_[numpy.mat(plane_v).T,rextra]
        line = numpy.r_[numpy.mat(line).T,rextra]
        """syms  y z
        eq1 = plane_c(2,1)*y+plane_c(3,1)*z+plane_c(4,1)==0
        eq2 = plane_c(2,2)*y+plane_c(3,2)*z+plane_c(4,2)==0
        A=numpy.solve(eq1,eq2,[y z])"""
        # 交线大多垂直于yoz平面，后续有待讨论plane(2,n)和plane(2,n+1)为0的情况

    # 遍历所有点找出离所选取平面最远的点和最近的点，并计算相应的打印厚度
    limit_value = limitpoint.limit_value(point_number, parts, plane_v)
    furthest = limit_value[0,0]
    thickest = numpy.abs(
        parts[0, furthest] * plane_c[0, 1] + parts[1, furthest] * plane_c[1, 1] + parts[2, furthest] * plane_c[2, 1] +
        plane_c[3, 1]) / (plane_c[0, 1] * plane_c[0, 1] + plane_c[1, 1] * plane_c[1, 1] + plane_c[2, 1] * plane_c[2, 1])
    nearest = limit_value[0,1]
    thinnest = numpy.abs(
        parts[0, nearest] * plane_c[0, 1] + parts[1, nearest] * plane_c[1, 1] + parts[2, nearest] * plane_c[2, 1] +
        plane_c[3, 1]) / (plane_c[0, 1] * plane_c[0, 1] + plane_c[1, 1] * plane_c[1, 1] + plane_c[2, 1] * plane_c[2, 1])
    thick_d_value = thickest - thinnest

    plane_vt = plane_v[0:3, 0]
    plane_vt = numpy.r_[plane_vt,parts[0:3, furthest]]  # 间距最大的平面
    # 判断法向量的方向是否指向所切区域
    # 小于等于0表示点到平面的距离为负值
    if plane_vt[0, 0] * point1_crood[3, 0] + plane_vt[1, 0] * point1_crood[4, 0] + plane_vt[2, 0] * point1_crood[
        5, 0] - (
            plane_vt[0, 0] * plane_vt[3, 0] + plane_vt[1, 0] * plane_vt[4, 0] + plane_vt[2, 0] * plane_vt[5, 0]) <= 0:
        plane_vt[0:3, 0] = -plane_v[0:3, 0]


    # 每移动一个直径距离的参数变化
    a = (2 * r * plane_vt[0, 0]) / numpy.sqrt(
        plane_vt[0, 0] * plane_vt[0, 0] + plane_vt[1, 0] * plane_vt[1, 0] + plane_vt[2, 0] * plane_vt[2, 0])
    b = (2 * r * plane_vt[1, 0]) / numpy.sqrt(
        plane_vt[0, 0] * plane_vt[0, 0] + plane_vt[1, 0] * plane_vt[1, 0] + plane_vt[2, 0] * plane_vt[2, 0])
    c = (2 * r * plane_vt[2, 0]) / numpy.sqrt(
        plane_vt[0, 0] * plane_vt[0, 0] + plane_vt[1, 0] * plane_vt[1, 0] + plane_vt[2, 0] * plane_vt[2, 0])

    num_translation = 0  # 代表平移几个距离，从0开始
    num_point_c = numpy.mat([[1]])  # 存储每个平行线的交点个数
    point_intersection = [parts[0: 3, furthest]]  # 存储具体的交点
    flag = 1
    #print(point_intersection)

    while 1:
        num_intersection = 0  # 代表交点个数，每次循环从0开始
        plane_vtp = plane_vt[:,0] + (num_translation + 1) * numpy.matrix([[0,0,0,a, b, c]]).T
        plane_vt = numpy.c_[plane_vt,plane_vtp]
        for i in range(point_number):  # 遍历所有点求交点
            if i != point_number-1:  # 如果不是最后一个点
                intersections = intersects.intersects(parts[:, i], parts[:, i + 1], plane_vt[:, num_translation + 1])
                #print(intersections)
                #intersections 是列向量不需要转置
                if intersections[3, 0] == 1:  # 交点如果存在, 存储该交点
                    num_intersection = num_intersection + 1
                    #考虑列的拓展问题
                    #如果是这一行的第一个点，需要拓展数组
                    if num_intersection == 1:
                        point_intersection.append(numpy.mat([[0.,0.,0.]]).T)
                        point_intersection[num_translation + 1][:,0]=intersections[0: 3, 0]
                    #如果不是这一行的第一个交点，需要拓展矩阵
                    else:
                        point_intersection[num_translation+1] = numpy.c_[point_intersection[num_translation+1],intersections[0: 3, 0]]

            else:
                intersections = intersects.intersects(parts[:, i], parts[:, 0], plane_vt[:, num_translation + 1])
                if intersections[3, 0] == 1:  # 交点如果存在, 存储该交点
                    num_intersection = num_intersection + 1
                    # 考虑列的拓展问题
                    if num_intersection == 1:
                        point_intersection.append(numpy.mat([[0, 0, 0]]).T)
                        point_intersection[num_translation + 1][:, 0] = intersections[0: 3, 0]
                    else:
                        point_intersection[num_translation + 1] = numpy.c_[
                            point_intersection[num_translation + 1], intersections[0: 3, 0]]
                    #print(point_intersection)
        # 将交点进行冒泡排序
        for i in range(num_intersection):
            for j in range(num_intersection - 1- i):  # 第j + 1减去j个点的向量如果和方向向量反向，则交换两点
                if numpy.dot(line[0:3, 0].T, (
                        point_intersection[num_translation + 1][:, j+1] - point_intersection[num_translation + 1][:,
                                                                            j])) * flag > 0:
                    #千万不要用零时变量，python中的赋值都是赋给地址
                    point_intersection[num_translation + 1][:, [j,j+1]] = point_intersection[num_translation + 1][:, [j+1,j]]

        # 在最近点左侧时退出循环
        if (plane_vt[0, num_translation + 1] * parts[0, nearest] + plane_vt[1, num_translation + 1] * parts[1, nearest] +
                plane_vt[2, num_translation + 1] * parts[2, nearest] - (
                plane_vt[0, num_translation + 1] * plane_vt[3, num_translation + 1] + plane_vt[1, num_translation + 1] *
                plane_vt[4, num_translation + 1] + plane_vt[2, num_translation + 1] * plane_vt[
                    5, num_translation + 1])) < 0:  # 判断法向量的方向是否指向所切区域
            break

        #迭代的循环变量
        num_point_c = numpy.c_[num_point_c,numpy.mat([[num_intersection]])]
        num_translation = num_translation + 1
        flag = -flag

    num_point_c = numpy.c_[num_point_c,numpy.mat([[1]])]
    point_intersection.append(numpy.mat([[0, 0, 0]]).T)
    point_intersection[num_translation + 1][:, 0] = parts[0:3, nearest]

    # 把所有点存储起来
    pathpoint = [numpy.mat([[0]])] #cell型第一位存储点的数量，第二位存储点的具体信息，第三位和第四位存储迭代信息
    pathpoint.append(numpy.mat([[0., 0.,0., 0., 0., 0., 0., 0.]]).T)
    pathpoint[1][0: 3, pathpoint[0][0, 0]] = point1_crood[0: 3]
    pathpoint[1][3: 6, 0] = point_intersection[0][:, 0]
    pathpoint[1][7, 0] = thickest
    pathpoint[1][6, pathpoint[0][0, 0]] = 0
    for i in range(1,num_translation + 1):
        for j in range(num_point_c[0, i]):
            pathpoint[0][0,0] = pathpoint[0][0,0] + 1
            pathpoint[1] = numpy.c_[pathpoint[1],numpy.mat([[0, 0, 0, 0, 0, 0, 0, 0]]).T]
            pathpoint[1][0: 3, pathpoint[0][0,0]] = point1_crood[0: 3]
            pathpoint[1][3: 6, pathpoint[0][0,0]] = point_intersection[i][:, j]
            pathpoint[1][7, pathpoint[0][0,0]] = thick.thick(thickest, thick_d_value, num_translation + 1, i-1)
            if (j == num_point_c[0, i] | numpy.mod(j, 2) == 1) & i != num_translation + 1:
                pathpoint[1][6, pathpoint[0][0,0]] = 1
            else:
                pathpoint[1][6, pathpoint[0][0,0]] = 0

    pathpoint[1][6,pathpoint[0][0,0]] = 0

    pathpoint.append(line[:, 0])
    pathpoint.append(plane_v[:, 0])

    return pathpoint
