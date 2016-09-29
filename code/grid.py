import math
from features import geo_len_delta

__all__ = [
    "max_range",
    "grid_map",
    "is_not_single",
    "crossing_cell",
    "cluster",
]


def max_range(tra):
    max_lng, max_lat = 0.0, 0.0
    min_lng, min_lat = 180.0, 90.0

    for line in tra:
        for pos in line:
            if len(pos) == 4:
                max_lng = float(pos[3]) if float(pos[3]) > max_lng else max_lng
                max_lat = float(pos[2]) if float(pos[2]) > max_lat else max_lat
                min_lng = float(pos[3]) if float(pos[3]) < min_lng else min_lng
                min_lat = float(pos[2]) if float(pos[2]) < min_lat else min_lat
    return max_lng, max_lat, min_lng, min_lat


def grid_map(n):
    grid = []

    for i in range(n):
        grid.append([])
        for j in range(n):
            grid[i].append([])

    return grid


def is_not_single(cell):
    if len(cell) >= 2:
        flag = cell[0]
        for item in cell:
            if item[0] != flag[0] and item[1] != flag[1]:
                return True
    return False


def crossing_cell(grid):
    repeat = []
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            tmp = []
            if is_not_single(grid[x][y]):
                tmp += [x, y]
                repeat.append(tmp)
    return repeat


def cluster(tra, min_lng, min_lat, interval):
    grid_cell = grid_map(200)
    print("Begin grid cluster ...")
    for line in tra:
        delta_len = 0
        lng_start, lat_start = float(line[0][3]), float(line[0][2])
        for i in range(len(line)):
            if len(line[i]) >= 4:
                if i >= 1:
                    lng_start, lat_start = float(line[i-1][3]), float(line[i-1][2])
                lng, lat= float(line[i][3]), float(line[i][2])
                x = math.floor((lng - min_lng) / interval)
                y = math.floor((lat - min_lat) / interval)
                
                tmp_len = abs(geo_len_delta(lng_start, lat_start, lng, lat))
                delta_len += tmp_len

                tmp = [int(line[i][0]), i, delta_len]
                line[i].append(tmp_len)

                x = x if x <= 199 else 199
                y = y if y <= 199 else 199
                
                grid_cell[x][y].append(tmp)

                # append the id of grid cell of trajectory to multi_list tra
                line[i].append([x, y]);
    print("End grid cluster ...")
    crossing = crossing_cell(grid_cell)
    return grid_cell, crossing
    