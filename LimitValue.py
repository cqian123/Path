"""
遍历所有点找出离所选取平面最远的点和最近的点
"""
import numpy
import conversion
def limitvalue(point_number, parts, plane_v):
    D = 0
    d = 200
    plane_vc =conversion.conversion(plane_v)
    for each in range(point_number):
        a = abs(plane_vc[0, 0]*parts[0, each]+plane_vc[1, 0]*parts[1, each]+plane_vc[2, 0]*parts[2, each]+plane_vc[3,0])
        b = numpy.sqrt(plane_vc[0, 0] ** 2 + plane_vc[1, 0] ** 2 + plane_vc[2, 0] ** 2)
        distance = a/b
        if each > 1:
            D = distance
            d = distance
            furthest = each
            nearest = each
        else:
            if distance>D:
                D = distance
                furthest = each
            if distance <d:
                d = distance
                nearest = each
    limit_value = numpy.mat([furthest, nearest])
    return limit_value

