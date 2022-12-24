"""
将骨骼点平面转换为平面方程的参数
"""
import numpy
def conversion(plane):
    a = plane[0, 0]
    b = plane[1, 0]
    c = plane[2, 0]
    d = -(plane[0, 0]*plane[3, 0]+plane[1, 0]*plane[4, 0]+plane[2, 0]*plane[5, 0])
    plane_c = numpy.matrix([a, b, c, d]).T
    return plane_c
