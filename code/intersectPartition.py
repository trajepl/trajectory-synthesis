import random
import copy
import math
from functools import reduce
import fileOperator
import grid
import features

__all__ = [
    "gene_partition",
    "standard",
    "max_deltax",
    "sub_grid_map",
    "link_sub_tra",
    "ip",
    "f",
]
# baseline2 which contains two conponents: 1 divide, 2 connect
# this methods contains two sub-methods 
# Node that: ip-divide is replace by gene_partiton in optimized methods
def ip_divide():

def ip_connect():

# optimized methods: gene partition
def gene_partition():
    num_gen_tra = 10000

    fea = ip.standard()
    for i in range(len(fea)):
        for j in range(len(fea[i])):
            fea[i][j] = math.ceil(num_gen_tra * float(fea[i][j]))
    
    filepath = "../falsedata/13K.txt"

    print("Begin read tra file ...")
    tra = fileOperator.read_file(filepath)
    print("End read tra file ...")

    write_path = "../resultdata/genTra3.txt"
    file_in = open(write_path, "w")
    
    print("Begin find max and min  ...")
    max_lng, max_lat, min_lng, min_lat = grid.max_range(tra)
    interval = max(max_lng - min_lng, max_lat - min_lat) / 200
    print("End find max and min  ...")

    grid = ip.sub_grid_map(tra, min_lng, min_lat, interval)
    repeat = grid.crossing_cell(grid)

    print("Begin update gen_part  ...")
    merge_sub_tra(tra, grid, repeat)
    ip_grid, ip_repeat = update_grid_repeat(tra)
    print("End updata gen_part  ...")

    count_tra = 0

    delta_x = [10, 6, 1, 10]
    print("Begin generate new tra...")
    for i in range(num_gen_tra):
        if len(ip_repeat) != 0:
            rand = random.randint(0, len(ip_repeat) - 1)
        point = ip_repeat[rand]
        point_inline = ip_grid[point[0]][point[1]]

        min_f = float('inf')
        flag_tra = tra[0]

        rand_inline = random.sample(point_inline, 1)
        x, y = rand_inline[0]
        sub0 = ip.sub_tra(tra, x, y, ip_grid)
        next_x, next_y = sub0[-1][4]

        length1 = len(point_inline) if len(point_inline) <= 20 else 20
        length2 = len(ip_grid[next_x][next_y]) if len(ip_grid[next_x][next_y]) <= 20 else 20

        for i in range(length1):
            index_px = random.randint(0, len(point_inline) - 1)
            px = point_inline[index_px]
            if px[0] != x and px[1] != 0 and px[1] != len(tra[px[0]]) - 1:

                sub_pre = ip.sub_tra(tra, px[0], px[1], ip_grid, False)
                sub_tra0 = ip.link_sub_tra(sub0, sub_pre, False)

                for j in range(length2):
                    index_px1 = random.randint(0, len(ip_grid[next_x][next_y]) - 1)
                    px1 = point_inline[index_px]

                    if px1[0] != next_x and px1[1] != 0 and px1[1] != len(tra[px1[0]]):
                        sub_next = ip.sub_tra(tra, px1[0], px1[1], ip_grid)
                        sub_tra0 = ip.link_sub_tra(sub_tra0, sub_next)

                        list_fea = list(features.features(sub_tra0))
                        tmp_f = ip.f(list_fea, delta_x)
                        if tmp_f < min_f:
                            flag_tra = sub_tra0
                            min_f = tmp_f
            
        line1 = ''

        for j in range(len(flag_tra)):
            line1 = line1 + str(count_tra) + ' ' + flag_tra[j][1] + ' ' + flag_tra[j][2] + ' ' + flag_tra[j][3] + '\n'
        file_in.write(line1)
        count_tra += 1

        delta_x = ip.max_deltax(fea)
        print(count_tra)
    file_in.close()
    print("End generate new tra...")

def standard():
    feature = [[0 for i in range(20)] for j in range(4)]
    i = 0
    for line in open("../resultdata/10K.txt", "r"):
        line = line.rstrip().split(' ')
        feature[0][i] = line[0]
        feature[1][i] = line[1]
        feature[2][i] = line[2]
        feature[3][i] = line[3]
        i += 1
    return feature

def max_deltax(fea):
    deltax = [10, 1, 1, 10]
    list_deltax = []

    for i in range(len(fea)):
        max_f = -1
        tmp = 0
        for j in range(len(fea[i])):
            if fea[i][j] > max_f:
                tmp = j+1
                max_f = fea[i][j]
        list_deltax.append(tmp)
        if fea[i][tmp] > 0:
            fea[i][tmp] -= 1

    for i in range(4):
        list_deltax[i] = deltax[i] * list_deltax[i]
    return list_deltax

def f(x, delta_x):
    b = []

    for i in range(3):
        b.append(abs((x[i] - delta_x[i]) / delta_x[i]))

    b.append(abs((x[-1] - (delta_x[-1] * x[0] / delta_x[0])) / delta_x[-1]))

    valuation = reduce((lambda x, y: x + y), b)
    return valuation


def sub_grid_map(tra, min_lng, min_lat, interval):
    # tmp_tra = copy.deepcopy(tra)
    tmp_tra = tra
    grid = grid.grid_map(200)

    for line in tmp_tra:
        for i in range(len(line)):
            if len(line[i]) == 4:
                x = int(math.floor((float(line[i][3]) - min_lng) / (interval * 1.0)))
                y = int(math.floor((float(line[i][2]) - min_lat) / (interval * 1.0)))
                line[i].append((x, y))

    for line in tmp_tra:
        for i in range(len(line)):
            if len(line[i]) == 5:
                tmp = [int(line[i][0]), i]
                x, y = line[i][4]
                x = x if x <= 199 else 199
                y = y if y <= 199 else 199
                grid[x][y].append(tmp)
    return grid


def link_sub_tra(tra_1, tra_2, towards=True):
    tra1 = copy.deepcopy(tra_1)
    tra2 = copy.deepcopy(tra_2)

    for m in range(len(tra2) - 1):
        s = features.addTime(features.toTime(tra1[-1][1]) + abs(features.toTime(tra_2[m][1]) - features.toTime(tra_2[m + 1][1])))
        tra2[m][1] = tra2[m][1].replace(tra2[m][1][6:], s)
        tra2[m][0] = tra1[m][0]
        if towards:
            tra1.append(tra2[m])
        else:
            tra1.insert(0, tra2[m])

    return tra1


def sub_tra(tra, x, y, grid, towards=True):
    tmp_sub_tra = []
    tmp_sub_tra.append(tra[x][y])
    grid_x0, grid_y0 = tra[x][y][4]

    if towards:
        while y < len(tra[x]) - 1:
            y += 1
            tmp_sub_tra.append(tra[x][y])
            grid_x, grid_y = tra[x][y][4]
            grid_x = 199 if grid_x > 199 else grid_x
            grid_y = 199 if grid_y > 199 else grid_y
            if len(grid[grid_x][grid_y]) >= 2 and (grid_x != grid_x0 or grid_y != grid_y0):
                break;
            grid_x0, grid_y0 = grid_x, grid_y
    else:
        while y > 1:
            y -= 1
            tmp_sub_tra.append(tra[x][y])
            grid_x, grid_y = tra[x][y][4]
            grid_x = 199 if grid_x > 199 else grid_x
            grid_y = 199 if grid_y > 199 else grid_y
            if len(grid[grid_x][grid_y]) >= 2 and (grid_x != grid_x0 or grid_y != grid_y0):
                break;
            grid_x0, grid_y0 = grid_x, grid_y

    return tmp_sub_tra


def ip():
    num_gen_tra = 1000

    fea = standard()
    for i in range(len(fea)):
        for j in range(len(fea[i])):
            fea[i][j] = math.ceil( num_gen_tra * float(fea[i][j]))

    filepath = "../falsedata/13K.txt"

    print("Begin read tra file ...")
    tra = fileOperator.read_file(filepath)
    print("End read tra file ...")

    write_path = "../resultdata/genTra2.txt"
    file_in = open(write_path, "w")

    print("Begin find max and min  ...")
    max_lng, max_lat, min_lng, min_lat = grid.max_range(tra)
    interval = max(max_lng - min_lng, max_lat - min_lat) / 200
    print("End find max and min  ...")

    grid = sub_grid_map(tra, min_lng, min_lat, interval)
    repeat = grid.crossing_cell(grid)

    count_tra = 0

    delta_x = [10, 6, 1, 10]
    print("Begin generate new tra...")
    for i in range(num_gen_tra):
        if len(repeat) != 0:
            rand = random.randint(0, len(repeat) - 1)
        point = repeat[rand]
        point_inline = grid[point[0]][point[1]]

        min_f = float('inf')
        flag_tra = tra[0]

        rand_inline = random.sample(point_inline, 1)
        x, y = rand_inline[0]
        sub0 = sub_tra(tra, x, y, grid)
        next_x, next_y = sub0[-1][4]

        length1 = len(point_inline) if len(point_inline) <= 20 else 20
        length2 = len(grid[next_x][next_y]) if len(grid[next_x][next_y]) <= 20 else 20

        for i in range(length1):
            index_px = random.randint(0, len(point_inline) - 1)
            px = point_inline[index_px]
            if px[0] != x and px[1] != 0 and px[1] != len(tra[px[0]]) - 1:

                sub_pre = sub_tra(tra, px[0], px[1], grid, False)
                sub_tra0 = link_sub_tra(sub0, sub_pre, False)

                for j in range(length2):
                    index_px1 = random.randint(0, len(grid[next_x][next_y]) - 1)
                    px1 = point_inline[index_px]

                    if px1[0] != next_x and px1[1] != 0 and px1[1] != len(tra[px1[0]]):
                        sub_next = sub_tra(tra, px1[0], px1[1], grid)
                        sub_tra0 = link_sub_tra(sub_tra0, sub_next)

                        list_fea = list(features.features(sub_tra0))
                        if list_fea[0] <= 0:
                            break
                        tmp_f = f(list_fea, delta_x)
                        if tmp_f < min_f:
                            flag_tra = sub_tra0
                            min_f = tmp_f
            
        line1 = ''

        for j in range(len(flag_tra)):
            line1 = line1 + str(count_tra) + ' ' + flag_tra[j][1] + ' ' + flag_tra[j][2] + ' ' + flag_tra[j][3] + '\n'
        file_in.write(line1)
        count_tra += 1

        delta_x = max_deltax(fea)
        print(count_tra)
    file_in.close()
    print("End generate new tra...")

if __name__ == "__main__":
    ip()
