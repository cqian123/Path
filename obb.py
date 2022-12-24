import numpy
import conversion
import limitpoint


#传入两层的信息
#返回第一层的方向包围盒的四个边界点的信息

def obb(point1_crood, point2_crood, line_p, plane_vp, parts):

    parts = numpy.mat(parts)
    plane_c = conversion.conversion(point1_crood)
    plane_c = numpy.c_[plane_c, conversion.conversion(point2_crood)]
    point_number = parts.shape[1]

    if numpy.all(numpy.dot(point1_crood[0:3].T,point2_crood[0:3]) >= 0.99):
        # 与后一个平面平行，0.99时法向量相乘的考虑到运算精度的问题
        line = line_p[0:6, 0]
        plane_v = plane_vp[0:6, 0]
    else:  # 交线存在
        # print(point1_crood,point1_crood[0:3, 0],point1_crood[0:3, 0].T,point2_crood)
        line = numpy.cross(point1_crood[0:3].T, point2_crood[0:3].T)
        # print(line)
        plane_v = numpy.cross(line[0, 0:3], point1_crood[0:3].T)  # 垂直于point1_crood且过直线line(:,1)的平面

        z = (plane_c[1, 0] * plane_c[3, 1] - plane_c[1, 1] * plane_c[3, 0]) / (
                    plane_c[2, 0] * plane_c[1, 1] - plane_c[2, 1] * plane_c[1, 0])
        y = (plane_c[2, 0] * plane_c[3, 1] - plane_c[3, 0] * plane_c[2, 1]) / (
                    plane_c[2, 1] * plane_c[1, 0] - plane_c[2, 0] * plane_c[1, 1])
        rextra = numpy.mat([[0, y, z]]).T
        plane_v = numpy.r_[numpy.mat(plane_v).T,rextra]
        line = numpy.r_[numpy.mat(line).T,rextra]

    #初始化矩阵,然后计算绕骨骼点旋转90度后的平面
    plane_vv = numpy.mat([[0, 0, 0, 0, 0, 0]]).T
    #先计算法向量
    plane_vv[0,0] = 1
    plane_vv[1, 0] = (point1_crood[0] * plane_v[2, 0] - point1_crood[2] * plane_v[0, 0]) / (
                point1_crood[2] * plane_v[1, 0] - point1_crood[1] * plane_v[3, 0])
    plane_vv[2, 0] = (point1_crood[0] * plane_v[1, 0] - point1_crood[1] * plane_v[0, 0]) / (
            point1_crood[1] * plane_v[2, 0] - point1_crood[2] * plane_v[1, 0])


    #然后再选取远处的一点,让选定的平面过这一点
    plane_vv[3,0] = 100+point1_crood[3]
    plane_vv[4, 0] = 100*(point1_crood[0] * (plane_v[5, 0]-point1_crood[5]) - point1_crood[2] * (plane_v[3, 0]-point1_crood[3]) ) / (
            point1_crood[2] * (plane_v[4, 0]-point1_crood[4]) - point1_crood[1] * (plane_v[5, 0]-point1_crood[5]))+point1_crood[4]
    plane_vv[5, 0] = 100*(point1_crood[0] * (plane_v[4, 0]-point1_crood[4]) - point1_crood[1] * (plane_v[3, 0]-point1_crood[3])) / (
            point1_crood[1] * (plane_v[4, 0]-point1_crood[4]) - point1_crood[2] * (plane_v[4, 0]-point1_crood[4]))+point1_crood[5]


    # 判断法向量的方向是否指向所切区域
    # 小于等于0表示点到平面的距离为负值

    if plane_vv[0, 0] * point1_crood[3] + plane_vv[1, 0] * point1_crood[4] + plane_vv[2, 0] * point1_crood[
        5] - (
            plane_vv[0, 0] * plane_vv[3, 0] + plane_vv[1, 0] * plane_vv[4, 0] + plane_vv[2, 0] * plane_vv[5, 0]) <= 0:
        plane_vv[0:3, 0] = -plane_vv[0:3, 0]



    #找到离plane_v最远和最近的点的序号
    limit_value = limitpoint.limit_value(point_number, parts, plane_v)
    #找到离plane_vv最远和最近的点的序号
    limit_value_v = limitpoint.limit_value(point_number, parts, plane_vv)

    line_eq = numpy.matrix(numpy.cross(point1_crood[0:3].T, plane_v[0:3].T))
    line_th = numpy.matrix(numpy.cross(point1_crood[0:3].T, plane_vv[0:3].T))

    obb_point = numpy.r_[limit_value.T, limit_value_v.T, line_th.T, line_eq.T]

    #前两个是厚度增加方向上的边界点的序号，后两个是厚度相同方向上的边界点序号
    #还有厚度变化方向的方向向量
    return obb_point



