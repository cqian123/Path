import numpy


def tran(pathpoint_final,Bone_Point):
    num1 = len(pathpoint_final)
    pathpoint_tran = []
    for n in range(num1):
        nor_vec_z = Bone_Point[0:3, n].T
        nor_vec_y = numpy.array([0,1,0])
        nor_vec_x = numpy.cross(nor_vec_y, nor_vec_z)
        matrix = numpy.array([nor_vec_x, nor_vec_y, nor_vec_z])
        R = numpy.linalg.inv(matrix)
        pathpoint_final[n][0, :] = pathpoint_final[n][0, :] - Bone_Point[3, n]
        pathpoint_final[n][1, :] = pathpoint_final[n][1, :] - Bone_Point[4, n]
        pathpoint_final[n][2, :] = pathpoint_final[n][2, :] - Bone_Point[5, n]

        parts1 = numpy.dot(pathpoint_final[n][0:3,:].T, R)
        parts1[:, 0] = parts1[:, 0] + Bone_Point[3, n]
        parts1[:, 1] = parts1[:, 1] + Bone_Point[4, n]
        parts1[:, 2] = parts1[:, 2] + Bone_Point[5, n]

        pathpoint_tran.append(parts1.T)

    return pathpoint_tran