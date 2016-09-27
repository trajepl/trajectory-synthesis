import random
import copy
import math
import os
import fileOperator
import grid
from functools import reduce

__all__=[

]

def swap_tra(tra1, tra2, i, j):
    tmp = []
    swap1 = copy.deepcopy(tra1)
    swap2 = copy.deepcopy(tra2)

    if len(tra1) - i > len(tra2) - j:
        for m in range(i + 1, len(tra1)):
            if j + m - i < len(tra2):
                tmp.append(swap1[m])
                if len(tra2) == 4:
                    s = addTime(toTime(tra1[m-1][1]) + toTime(tra2[j + m - i][1]) - toTime(tra2[j + m - i - 1][1]))
                    tra1[m][1] = tra1[m][1].replace(tra1[m][1][6:], s)
                    tra1[m][2] = tra2[j + m - i][2]
                    tra1[m][3] = tra2[j + m - i][3]
            else:
                if len(tra1) > m:
                    tmp.append(swap1[m])
                    tra1.pop(m)

        for n in range(j + 1, len(tmp) + j + 1):
            if n < len(tra2):
                if len(tmp) == 4:
                    s = addTime(toTime(tra2[n-1][1]) + toTime(tmp[n - j - 1][1]) - toTime(tmp[n - j - 2][1]))
                    tra2[n][1] = tra2[n][1].replace(tra2[n][1][6:], s)
                    tra2[n][2] = tmp[n - j - 1][2]
                    tra2[n][3] = tmp[n - j - 1][3]
            else:
                tra2.append(tmp[n - j - 1])
    else:
        for m in range(j + 1, len(tra2)):
            if i + m - j < len(tra1):
                tmp.append(swap2[m])
                if len(tra1) == 4:
                    s = addTime(toTime(tra2[m-1][1]) + toTime(tra1[i + m - j][1]) - toTime(tra1[i + m - j - 1][1]))
                    tra2[m][1] = tra2[m][1].replace(tra2[m][1][6:],  s)
                    tra2[m][2] = tra1[i + m - j][2]
                    tra2[m][3] = tra1[i + m - j][3]
            else:
                if m < len(tra2):
                    tmp.append(swap2[m])
                    tra2.pop(m)

        for n in range(i + 1, len(tmp) + i + 1):
            if n < len(tra1):
                if len(tmp) == 4:
                    s = addTime(toTime(tra1[n-1][1]) + toTime(tmp[n - i - 1][1]) - toTime(tmp[n - i - 2][1]))
                    tra1[n][1] = tra1[n][1].replace(tra1[n][1][6:], s)
                    tra1[n][2] = tmp[n - i - 1][2]
                    tra1[n][3] = tmp[n - i - 1][3]
            else:
                tra1.append(tmp[n - i - 1])
    return tra1, tra2

# baseline1: random generation
def random_generation(filepath, write_path):
	# filepath = "../falsedata/13K.txt"

    tra = fileOperator.read_file(filepath);

    # write_path = "../resultdata/genTra1.txt"
    file_in = open(write_path, "w")

    print("Begin find max and min  ...")
    max_lng, max_lat, min_lng, min_lat = grid.max_range(tra)
    interval = (max(max_lng - min_lng, max_lat - min_lat) / 200)
    print("End find max and min  ...")

	
	crossing, grid = grid.cluster();
	print("Begin generate new tra...")
    for i in range(5000):
        rand = random.randint(0, len(repeat)-1)
        point = repeat[rand]
        point_inline = grid[point[0]][point[1]]
        rand_inline = random.sample(point_inline, 2)
        tra1 = tra[rand_inline[0][0]]
        tra2 = tra[rand_inline[1][0]]
        tra1, tra2 = swap_tra(tra1, tra2, rand_inline[0][1], rand_inline[1][1])
        line1, line2 = '', ''

        for j in range(len(tra1)):
            if len(tra1[j]) == 4:
                line1 = line1 + str(count_tra) + ' ' + tra1[j][1] + ' ' + tra1[j][2] + ' ' + tra1[j][3] + '\n'

        count_tra += 1
        for j in range(len(tra2)):
            if len(tra2[j]) == 4:
                line2 = line2 + str(count_tra) + ' ' + tra2[j][1] + ' ' + tra2[j][2] + ' ' + tra2[j][3] + '\n'
        file_in.write(line1 + line2)
        count_tra += 1

    file_in.close()
    print("End generate new tra...") 