import numpy
import matplotlib.pyplot as plt
import pyclipper
import conversion
import My_clipper

def offset(parts,Bone_Point,Bone_Point2, r):
    # R = RotationMatrix.Rotataion(Bone_Point[0:3,0])
    # 3*3darray
    nor_vec_z = Bone_Point[0:3,0].T.getA()
    nor_vec_z = nor_vec_z[0]
    nor_vec_x = (parts[0,:] - parts[1,:]) / \
                numpy.sqrt(numpy.inner((parts[0,:] - parts[1,:]), (parts[0,:] - parts[1,:])))
    nor_vec_y = numpy.cross(nor_vec_z, nor_vec_x)
    matrix = numpy.array([nor_vec_x, nor_vec_y, nor_vec_z])
    R = numpy.linalg.inv(matrix)
    parts[:, 0] = parts[:, 0] - Bone_Point[3, 0]
    parts[:, 1] = parts[:, 1] - Bone_Point[4, 0]
    parts[:, 2] = parts[:, 2] - Bone_Point[5, 0]
    # R1 = linalg.solve(numpy.mat([[0,0,1]]), Bone_Point[0:3,0].T)
    # b = numpy.dot(Bone_Point[0:3,0].T,R)
    # b1 = numpy.dot(Bone_Point[0:3,0].T,R1)
    parts1 = numpy.dot(parts,R)
    parts1 *= 1000
    #clipper库只能处理整数，故将其放大1000倍进行运算以提高其精度
    num1 = parts1.shape[0]

    # parts1 = [round(x) for x in parts[0]]
    # parts1 = parts.tolist()

    parts2 = parts1[:,[0, 1]]
    # zextra = parts1[:,2]
    # zextra = numpy.expand_dims(zextra,axis=0)
    # parts4 = parts3.getA()
    # parts3 = parts2.astype(numpy.int32)


    '''
    #parts2.astype(numpy.int32)
    solution = My_clipper.clipper(parts2,r*1000)
    if solution == []:
        parts[:, 0] = parts[:, 0] + Bone_Point[3, 0]
        parts[:, 1] = parts[:, 1] + Bone_Point[4, 0]
        parts[:, 2] = parts[:, 2] + Bone_Point[5, 0]
        pathpoint = []
        return pathpoint
    pathpoint1 = solution.T
    '''


    parts3 = parts2.tolist()
    parts4 = []
    for i in range(num1):
        parts4.append(tuple(parts3[i]))

    parts5 = tuple(parts4)
        # clipper 剪切处理的是元组类型的二维点数据，所以需要转化点的数据类型

    pco = pyclipper.PyclipperOffset()
    pco.AddPath(parts5, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

    solution = pco.Execute(-r*1000.0)
    pathpoint = numpy.asarray(solution)

    # print(solution)
    if solution == []:
        parts[:, 0] = parts[:, 0] + Bone_Point[3, 0]
        parts[:, 1] = parts[:, 1] + Bone_Point[4, 0]
        parts[:, 2] = parts[:, 2] + Bone_Point[5, 0]
        pathpoint = []
        return pathpoint

    pathpoint1 = pathpoint[0].T
    #别人的代码，到这里结束


    # pathpoint2 = numpy.hstack((pathpoint1, zextra))
    num2 = pathpoint1.shape[1]
    zextra = numpy.zeros((1,num2))
    pathpoint2 = numpy.concatenate((pathpoint1, zextra),axis=0)
    pathpoint2 = numpy.dot(R,pathpoint2)
    pathpoint2 = pathpoint2 / 1000
    pathpoint2[0,:] = pathpoint2[0,:]+Bone_Point[3, 0]
    pathpoint2[1,:] = pathpoint2[1,:]+Bone_Point[4, 0]
    pathpoint2[2,:] = pathpoint2[2,:]+Bone_Point[5, 0]
    '''pathpoint3 = numpy.ones((3,num2))
    pathpoint3[0, :] = pathpoint3[0, :] * Bone_Point[0, 0]
    pathpoint3[1, :] = pathpoint3[1, :] * Bone_Point[1, 0]
    pathpoint3[2, :] = pathpoint3[2, :] * Bone_Point[2, 0]
    pathpoint3 = numpy.r_[pathpoint3,pathpoint2]
    pathpoint3 = numpy.r_[pathpoint3, numpy.ones((1,num2))]
    #pathpoint3[6,num2-1] = 0'''
    pathpoint3 = numpy.r_[pathpoint2, numpy.zeros((1,num2))]
    parts[:, 0] = parts[:, 0] + Bone_Point[3, 0]
    parts[:, 1] = parts[:, 1] + Bone_Point[4, 0]
    parts[:, 2] = parts[:, 2] + Bone_Point[5, 0]

    '''
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.xlabel('x')
    plt.ylabel('y')
    x = pathpoint3[0, :]
    y = pathpoint3[1, :]
    z = pathpoint3[2, :]
    ax.plot3D(x, y, z, 'r-')

    ax.legend()
    plt.show()
    '''

    BP_v = conversion.conversion(Bone_Point2)
    for i in range(num2):
        pathpoint3[3,i] = numpy.abs(pathpoint3[0,i]*BP_v[0,0]+pathpoint3[1,i]*BP_v[1,0]+pathpoint3[2,i]*BP_v[2,0]+BP_v[3,0])/numpy.sqrt(BP_v[0,0]*BP_v[0,0]+BP_v[1,0]*BP_v[1,0]+BP_v[2,0]*BP_v[2,0])

    return pathpoint3

