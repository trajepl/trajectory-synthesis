import random
import copy
import math
import os

__all__ = [
	'',
]

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

def grid_map(count):
	grid = []

	for i in range(n):
		grid.append([]);
		for j in range(n):
			grid[i].append([])

	return grid

def is_single(cell):
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
            if isNotSingle(grid[x][y]):
                tmp += [x, y]
                repeat.append(tmp)
    return repeat

def cluster(tra):
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

    crossing = crossing_cell(grid);

    return grid, crossing


