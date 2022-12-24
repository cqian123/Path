import numpy

def sort(pathpoint_all):
    pathpoint_final = []
    num1 = len(pathpoint_all)
    for i in range(num1):
        num2 = len(pathpoint_all[i][0])
        for j in range(num2):
            # print(pathpoint_all[i][:,j])
            pathpoint_final.append(pathpoint_all[i][:, j])

    return pathpoint_final