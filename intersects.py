"""
求两点构成的线段与平面交点的函数
"""
import numpy
import conversion
def intersects(point1, point2, plane_i):
    plane_ci = conversion.conversion(plane_i)
    segment = point2 - point1
    #print(plane_i)
    if numpy.dot(segment.T,plane_i[0:3,0]) != 0:
        P1D = plane_ci[0, 0] * point1[0, 0] + plane_ci[1, 0] * point1[1, 0] + plane_ci[2, 0] * point1[2, 0] + plane_ci[3, 0]
        if P1D != 0:
            P1D2 = plane_ci[0, 0] * segment[0, 0] + plane_ci[1, 0] * segment[1, 0] + plane_ci[2, 0] * segment[2, 0]
            N = -P1D/P1D2
            intersections = point1[:, 0]+N * segment
            if numpy.dot(N*segment.T,(1-N)*segment) > 0:
                intersections = numpy.r_[intersections, numpy.mat([[1]])]
            else:
                intersections = numpy.r_[intersections, numpy.mat([[0]])]
        else:
            intersections = point1
            intersections = numpy.r_[intersections, numpy.mat([[1]])]
    else:
        intersections = numpy.mat([[0,0,0,0]]).T
    return intersections