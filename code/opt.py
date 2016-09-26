import baseline1 as rg
import baseline2 as ip
import features
import random
import math

def Sim(tra_f1, tra_f2):
    a = sum([tra_f1[i] * tra_f2[i] for i in range(len(tra_f1))])
    b = math.sqrt(sum([x ** 2 for x in tra_f1]))
    c = math.sqrt(sum([y ** 2 for y in tra_f2]))

    if b != 0 and c != 0:
        return a / (b * c)
    return 0

def merge_sub_tra(tra, grid, repeat_grid):
    for repeat_point in repeat_grid:
        x1, y1 = repeat_point
        for x, y in grid[x1][y1]:
            tra[x][y].append('0')
    print("...End update station 1...")
    sub1, sub2 = [], []
    flag = 0
    for line in tra:
        for point in line:
            if len(point) <= 5 or flag == 0:
                sub1.append(point)
                flag = 1
            elif len(point) > 5:
                sub1.append(point)
                tmp = sub1
                sub1 = sub2
                sub2 = tmp
                list_fea1 = list(features.features(sub1))
                list_fea2 = list(features.features(sub2))
                if Sim(list_fea1[1:3], list_fea2[1:3]) > math.sqrt(2) / 2:
                    point[-1] = '1'
                sub1 = []

def update_grid_repeat(tra):
    ip_grid = rg.grid_map(200)
    for line in tra:
        for i in range(len(line)):
            if len(line[i]) > 5:
                tmp = [int(line[i][0]), i]
                x,y = line[i][4]
                x = x if x <= 199 else 199
                y = y if y <= 199 else 199
                ip_grid[x][y].append(tmp)

    ip_repeat = rg.repeat_grid(ip_grid)
    return ip_grid, ip_repeat


def gp():
    num_gen_tra = 10000

    fea = ip.standard()
    for i in range(len(fea)):
        for j in range(len(fea[i])):
            fea[i][j] = math.ceil(num_gen_tra * float(fea[i][j]))
    
    filepath = "../falsedata/13K.txt"

    print("Begin read tra file ...")
    tra = rg.read_file(filepath)
    print("End read tra file ...")

    write_path = "../resultdata/genTra3.txt"
    base1 = open(write_path, "w")

    print("Begin find max and min  ...")
    max_lng, max_lat, min_lng, min_lat = rg.max_range(tra)
    interval = max(max_lng - min_lng, max_lat - min_lat) / 200
    print("End find max and min  ...")

    grid = ip.sub_grid_map(tra, min_lng, min_lat, interval)
    repeat = rg.repeat_grid(grid)

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
        base1.write(line1)
        count_tra += 1

        delta_x = ip.max_deltax(fea)
        print(count_tra)
    base1.close()
    print("End generate new tra...")

if __name__ == "__main__":
    gp()
