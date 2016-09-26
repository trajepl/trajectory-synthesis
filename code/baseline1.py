import random
import copy
import math
import os

def max_range(tra):
    max_lng, max_lat = 0.0, 0.0
    min_lng, min_lat = 180.0, 90.0
    count = 0
    for line in tra:
        for pos in line:
            if len(pos) == 4:
                max_lng = float(pos[3]) if float(pos[3]) > max_lng else max_lng
                max_lat = float(pos[2]) if float(pos[2]) > max_lat else max_lat
                min_lng = float(pos[3]) if float(pos[3]) < min_lng else min_lng
                min_lat = float(pos[2]) if float(pos[2]) < min_lat else min_lat
    return max_lng, max_lat, min_lng, min_lat

def toTime(time):
    return int(time[-1]) + int(time[-2]) * 10 + (int(time[-3]) + int(time[-4]) * 10) * 60 + (int(time[-5]) + int(time[-6]) * 10) * 3600 + (int(time[-7]) + int(time[-8])) * 24 * 3600

def addTime(time):
    day = time // (3600 * 24)
    time -= 24 * 3600 * day
    h = time // 3600
    time -= 3600 * h
    minutes = time // 60
    seconds = time - minutes * 60

    time_str = ''
    if day <= 9:
        time_str += '0' + str(day)
    else:
        time_str += str(day)
    if h <= 9:
        time_str += '0' + str(h)
    else:
        time_str += str(h)
    if minutes <= 9:
        time_str += '0' + str(minutes)
    else:
        time_str += str(minutes)
    if seconds <= 9:
        time_str += '0' + str(seconds)
    else:
        time_str += str(seconds)
    if len(time_str) == 8:
        return time_str

def read_file(filepath):
    traje_file = open(filepath, 'r')
    matrix = []
    matrix.append([])
    count = 0
    line = traje_file.readline().strip().split(' ')
    first = line

    global count_tra

    matrix[count].append(line)

    while len(line) >= 2:
        line = traje_file.readline().strip().split(' ')
        if first[0] == line[0]:
            matrix[count].append(line)
        else:
            count += 1
            matrix.append([])
            first = line
            matrix[count].append(line)
            count_tra += 1
            if count_tra > 10000:
                break

    traje_file.close()
    return matrix

def grid_map(n):
    grid = []
    for i in range(n):
        grid.append([])
        for j in range(n):
            grid[i].append([])
    return grid

def isNotSingle(point):
    if len(point) >= 2:
        flag = point[0]
        for line in point:
            if line[0] != flag[0] and line[1] != flag[1]:
                return True
    return False

def repeat_grid(grid):
    repeat = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            tmp = []
            if isNotSingle(grid[x][y]):
                tmp += [x, y]
                repeat.append(tmp)
    return repeat


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

def main():
    filepath = "../falsedata/13K.txt"

    print("Begin read tra file ...")
    tra = read_file(filepath)
    print("End read tra file ...")

    write_path = "../resultdata/genTra1.txt"
    base1 = open(write_path, "w")

    print("Begin find max and min  ...")
    max_lng, max_lat, min_lng, min_lat = max_range(tra)
    interval = (max(max_lng - min_lng, max_lat - min_lat) / 200)
    print("End find max and min  ...")

    grid = grid_map(200)

    for line in tra:
        for i in range(len(line)):
            if len(line[i]) == 4:
                x = math.floor((float(line[i][3]) - min_lng) / interval)
                y = math.floor((float(line[i][2]) - min_lat) / interval)
                tmp = [int(line[i][0]), i]
                x = x if x <= 199 else 199
                y = y if y <= 199 else 199
                grid[x][y].append(tmp)

    repeat = repeat_grid(grid)

    count_tra = 0
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
        base1.write(line1 + line2)
        count_tra += 1

    base1.close()
    print("End generate new tra...")

count_tra = 0

if __name__ == '__main__':
    main()
