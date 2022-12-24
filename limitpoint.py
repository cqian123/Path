import numpy
import conversion

#遍历所有点找出离所选取平面最远的点和最近的点
def limit_value(point_number,parts,plane_v):
    D = 0
    d = 200
    plane_vc = conversion.conversion(plane_v)
    #print(point_number,parts,plane_v)
    for i in range(point_number):
        distance=numpy.abs(plane_vc[0,0]*parts[0,i]+plane_vc[1,0]*parts[1,i]+plane_vc[2,0]*parts[2,i]+plane_vc[3,0])/numpy.sqrt(plane_vc[0,0]*plane_vc[0,0]+plane_vc[1,0]*plane_vc[1,0]+plane_vc[2,0]*plane_vc[2,0])
        if i>=2: #内存空间可以释放，有待优化
            if distance>D:
                D = distance
                furthest = i
            if distance<d:
                d = distance
                nearest = i
        else:
            D =distance
            d =distance
            furthest = i
            nearest = i
    limit_value = numpy.matrix([[furthest,nearest]])
    return limit_value