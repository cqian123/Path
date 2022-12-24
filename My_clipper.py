import numpy
import math
#传入46*2ndarray的二维平面点的数据

def clipper(parts,r):
    num1 = parts.shape[0]

    #利用原点来给所有点顺时针冒泡排序
    degree = numpy.zeros((1,num1))
    for i in range(num1):
        degree[0,i] = math.degrees(math.acos(parts[i,0] / math.sqrt(parts[i,0]*parts[i,0]+parts[i,1]*parts[i,1]+100)))

    for i in range(num1):
        for j in range(num1-1-i):
            if (parts[j,1]>0) and (parts[j+1,1]>0) and (degree[0,j]<degree[0,j+1]):
                degree[0,[j,j+1]]= degree[0,[j+1,j]]
                parts[[j,j+1],:]=parts[[j+1,j],:]
            elif (parts[j,1]>0) and (parts[j+1,1]<0):
                degree[0,[j,j+1]]= degree[0,[j+1,j]]
                parts[[j,j+1],:]=parts[[j+1,j],:]
            elif (parts[j,1]<0) and (parts[j+1,1]<0) and (degree[0,j]>degree[0, j+1]):
                degree[0,[j,j+1]]= degree[0,[j+1,j]]
                parts[[j,j+1],:]=parts[[j+1,j],:]
                #print(parts[i + 1,:], parts[i,:])

    #创建深拷贝来判断向量是否反向
    parts1 = numpy.array(parts, copy=True)
    line_kb = numpy.zeros((num1,2))
    line_kb_off = numpy.zeros((num1, 2))
    parts_off = numpy.zeros((num1,2))
    #vector_1 = numpy.matrix([(parts1[0,0]-parts1[num1-1,0]),(parts1[0,1]-parts1[num1-1,1])])


    for i in range(num1):
        #最后一条交线时不是i+1与i相减
        if i == num1-1:
            # 判断直线斜率是否存在，如果斜率不存在，记斜率为10000，与x轴交点为b
            # 如果斜率存在则记斜率为K,与y轴的交点为b
            if (parts[0, 0] - parts[i, 0]) == 0:
                line_kb[i, 0] = 10000
                line_kb[i, 1] = parts[i, 0]
            else:
                line_kb[i, 0] = (parts[0, 1] - parts[i, 1]) / (parts[0, 0] - parts[i, 0])
                line_kb[i, 1] = parts[i, 1] - line_kb[i, 0] * parts[i, 0]
        else:
            if (parts[i + 1, 0] - parts[i, 0]) == 0:
                line_kb[i, 0] = 10000
                line_kb[i, 1] = parts[i, 0]
            else:
                line_kb[i, 0] = (parts[i + 1, 1] - parts[i, 1]) / (parts[i + 1, 0] - parts[i, 0])
                line_kb[i, 1] = parts[i, 1] - line_kb[i, 0] * parts[i, 0]


    #向内平移r，假设点是顺时针排列的
    for i in range(num1):
        detab = r*numpy.sqrt(1+line_kb[i,0]*line_kb[i,0])
        # 最后一条交线时不是i+1与i相减
        if i == num1 - 1:
        #如果横坐标较大则b减小r*根号下(1+k^2)
            if (parts[0, 0]-parts[i, 0]) == 0:
                #如果斜率不存在，则根据原点判定，因为原点是中心
                if line_kb[i,1] < 0:
                    line_kb_off[i,1] = line_kb[i,1] + r
                else:
                    line_kb_off[i, 1] = line_kb[i, 1] - r
            else:
                if line_kb[i, 1] > 0:
                    line_kb_off[i, 1] = line_kb[i, 1] - detab
                else:
                    line_kb_off[i, 1] = line_kb[i, 1] + detab
        #不是最后一条时有
        else:
            if (parts[i+1, 0]-parts[i, 0]) == 0:
                #如果斜率不存在，则根据原点判定，因为原点是中心
                if line_kb[i,1] < 0:
                    line_kb_off[i,1] = line_kb[i,1] + r
                else:
                    line_kb_off[i, 1] = line_kb[i, 1] - r
            else:
                if line_kb[i, 1] > 0:
                    line_kb_off[i, 1] = line_kb[i, 1] - detab
                else:
                    line_kb_off[i, 1] = line_kb[i, 1] + detab

    for i in range(num1):
        line_kb_off[i,0] = line_kb[i,0]
        if (line_kb_off[i, 1] * line_kb[i, 1])<0:
            return []


    #最后通过循环求各个直线之间的交点
    for i in range(num1):
        #先判断是否为第一个点，第i和i+1个点构成第i条线，所以第i和i-1条线交点为第i个点
        if i == 0:
            if line_kb_off[num1-1, 0] == 10000:
                parts_off[0, 0] = line_kb_off[num1-1, 1]
                parts_off[0, 1] = line_kb_off[0, 0]*parts_off[i, 0]+line_kb_off[0, 1]
            elif line_kb_off[0, 0] == 10000:
                parts_off[0, 0] = line_kb_off[0, 1]
                parts_off[0, 1] = line_kb_off[num1-1, 0]*parts_off[0, 0]+line_kb_off[num1-1, 1]
            else:
                parts_off[0, 0] = (line_kb_off[0, 1]-line_kb_off[num1-1, 1])/(line_kb_off[num1-1, 0]-line_kb_off[0, 0])
                parts_off[0, 1] = line_kb_off[num1-1, 0]*parts_off[0, 0]+line_kb_off[num1-1, 1]
        else:
            if line_kb_off[i - 1, 0] == 10000:
                parts_off[i, 0] = line_kb_off[i - 1, 1]
                parts_off[i, 1] = line_kb_off[i, 0] * parts_off[i, 0] + line_kb_off[i, 1]
            elif line_kb_off[i, 0] == 10000:
                parts_off[i, 0] = line_kb_off[i, 1]
                parts_off[i, 1] = line_kb_off[i - 1, 0] * parts_off[i, 0] + line_kb_off[i - 1, 1]
            else:
                parts_off[i, 0] = (line_kb_off[i, 1] - line_kb_off[i - 1, 1]) / (line_kb_off[i - 1, 0] - line_kb_off[i, 0])
                parts_off[i, 1] = line_kb_off[i, 0] * parts_off[i, 0] + line_kb_off[i, 1]

    vector_2 = numpy.matrix([(parts_off[0, 0] - parts_off[num1 - 1, 0]), (parts_off[0, 1] - parts_off[num1 - 1, 1])])

    # 利用原点来给所有点顺时针冒泡排序
    degree_off = numpy.zeros((1, num1))
    for i in range(num1):
        degree_off[0, i] = math.degrees(
            math.acos(parts_off[i, 0] / math.sqrt(
                parts_off[i, 0] * parts_off[i, 0] + parts_off[i, 1] * parts_off[i, 1] + 100)))

    for i in range(num1):
        for j in range(num1 - 1 - i):
            if (parts_off[j, 1] > 0) and (parts_off[j + 1, 1] > 0) and (degree_off[0, j] < degree_off[0, j + 1]):
                degree_off[0, [j, j + 1]] = degree_off[0, [j + 1, j]]
                parts_off[[j, j + 1], :] = parts_off[[j + 1, j], :]
            elif (parts_off[j, 1] > 0) and (parts_off[j + 1, 1] < 0):
                degree_off[0, [j, j + 1]] = degree_off[0, [j + 1, j]]
                parts_off[[j, j + 1], :] = parts_off[[j + 1, j], :]
            elif (parts_off[j, 1] < 0) and (parts_off[j + 1, 1] < 0) and (degree_off[0, j] > degree_off[0, j + 1]):
                degree_off[0, [j, j + 1]] = degree_off[0, [j + 1, j]]
                parts_off[[j, j + 1], :] = parts_off[[j + 1, j], :]
    return parts_off

    '''  
    #判定返回空集的条件
    if numpy.dot(vector_1,vector_2.T) < 0:
        return []
    else:

        # 利用原点来给所有点顺时针冒泡排序
        degree_off = numpy.zeros((1, num1))
        for i in range(num1):
            degree_off[0, i] = math.degrees(
                math.acos(parts_off[i, 0] / math.sqrt(parts_off[i, 0] * parts_off[i, 0] + parts_off[i, 1] * parts_off[i, 1] + 100)))

        for i in range(num1):
            for j in range(num1 - 1 - i):
                if (parts_off[j, 1] > 0) and (parts_off[j + 1, 1] > 0) and (degree_off[0, j] < degree_off[0, j + 1]):
                    degree_off[0, [j, j + 1]] = degree_off[0, [j + 1, j]]
                    parts_off[[j, j + 1], :] = parts_off[[j + 1, j], :]
                elif (parts_off[j, 1] > 0) and (parts_off[j + 1, 1] < 0):
                    degree_off[0, [j, j + 1]] = degree_off[0, [j + 1, j]]
                    parts_off[[j, j + 1], :] = parts_off[[j + 1, j], :]
                elif (parts_off[j, 1] < 0) and (parts_off[j + 1, 1] < 0) and (degree_off[0, j] > degree_off[0, j + 1]):
                    degree_off[0, [j, j + 1]] = degree_off[0, [j + 1, j]]
                    parts_off[[j, j + 1], :] = parts_off[[j + 1, j], :]
        return parts_off
    '''