# from grid import *
from fileOperator import *
from features import *
import random
import copy


def add_tra_flag(tra):
	for line in tra:
		for position in line:
			position.append(0)


def init_tra_flag(tra):
	for line in tra:
		for position in line:
			position[-1] = 0


def synthesize(tra, grid):
	global count_tra
	# is_single(cell) 
	connect_id = random.randint(0, count_tra)
	sum_tra = copy.deepcopy(tra[connect_id])
	# get the locate of grid_map
	last_point = tra[connect_id][-1][-1]
	
	add_tra_flag(tra)

	x, y = int(last_point[0]), int(last_point[1])
	cell = grid[x][y]

	# print(is_not_single(cell) and not tra[connect_id][-1][-1])
	time_end = sum_tra.pop()[1]

	while(is_not_single(cell) and tra[connect_id][-1][-1] == 0):
		for item in tra[connect_id]:
			item[-1] = 1

		tmp = random.choice(cell)
		for item in cell:
			if tmp[0] == connect_id:
				tmp = random.choice(cell)
			else:
				break

		connect_id = tmp[0]
		start_point = tra[connect_id][tmp[1]][1].strip()
		tra[connect_id][tmp[1]][1] = time_end

		for i in range(tmp[1], len(tra[connect_id])-1):
			origin_point = tra[connect_id][i][1].strip()
			end_point = tra[connect_id][i+1][1].strip()

			# print(start_point, end_point, origin_point)

			# time_connect
			start = toTime(start_point)
			end = toTime(end_point)
			origin = toTime(origin_point)
			
			s = addTime(origin + end - start)
			if not s:
				break
			
			origin_point_tmp = origin_point.replace(origin_point[6:], str(s))

			# id change
			start_point = tra[connect_id][i+1][1].strip()			
			tra[connect_id][i+1][1] = origin_point_tmp
			tra[connect_id][i][0] = sum_tra[0][0]

			# print(tra[connect_id][i])
			tra[connect_id][i][-1] = 1
			sum_tra.append(tra[connect_id][i])


		last_point = tra[connect_id][-1][-2]

		x, y = int(last_point[0]),int(last_point[1])
		cell = grid[x][y]
		
		time_end = sum_tra[-1][1]
		print(time_end)
	
	init_tra_flag(tra)
	
	# for line in sum_tra:
	# 	print(line)
	return sum_tra

def distribute_rate(item):
	sum_rate = 0
	for line in item:
		sum_rate += int(line)

	rate = []
	for i in range(len(item)):
		rate.append(item[i] / sum_rate)
	return rate

def shuffle_seque(n, rate):
	number_goal = []
	sequence = []
	cnt = 1
	for item in rate:
		number_goal.append(round(n*item))
		for i in range(number_goal[-1]):
			sequence.append(random.randint(10000*(cnt-1), 10000*cnt))
		cnt += 1

	random.shuffle(sequence)
	# print(sequence)
	return sequence

def append_sum(sum_tra):
	sum_length = 0
	
	for line in sum_tra:
		sum_length += line[4]
		line[4] = sum_length


if __name__ == '__main__':
	# generate histories trajectories
	filepath = "../falsedata/13K.txt"
	writepath = "../resultdata/extend.txt"
	number_goal = 1000
	count_cell = 200

	global count_tra

	tra = read_file(filepath)

	grid_cell = grid_map(count_cell)

	print("Begin find max and min  ...")
	max_lng, max_lat, min_lng, min_lat = max_range(tra)
	interval = (max(max_lng - min_lng, max_lat - min_lat) / 200)
	print("End find max and min  ...")

	grid, repeat = cluster(tra, min_lng, min_lat, interval)

	print("Begin get features and get the sequence ...")
	length = length_features(tra, grid)
	length_rate = distribute_rate(length)

	sequence = shuffle_seque(number_goal, length_rate)
	print("End get features and get the sequence ...")

	tra_tmp = copy.deepcopy(tra)
	print("Begin synthesize sum_tra ...")
	sum_tra = synthesize(tra, grid)
	append_sum(sum_tra)
	print("End synthesize sum_tra ...")

	# dividing the new long trajectories
	new_tra = [[]]
	new_cnt = 0
	point_cnt = 0
	first_id = 0
	count = 0

	for item in sequence:
		count += 1
		while point_cnt < len(sum_tra):
			# print("Note that: ", item, "First-id: ", first_id, "point-cnt: ", point_cnt)
			# print(sum_tra[point_cnt][4] - sum_tra[first_id][4], item)
			if sum_tra[point_cnt][4] - sum_tra[first_id][4] > item:
				print("dividing", '\n')
				first_id = point_cnt
				new_cnt += 1
				new_tra.append([])
				break
			# print(new_cnt, point_cnt, len(sum_tra), item, first_id)
			new_tra[-1].append(sum_tra[point_cnt])
			point_cnt += 1
		if new_cnt >= number_goal:
			print("finish apart", '\n')
			break
		elif point_cnt < len(sum_tra):
			continue
		else:
			print("do it again", '\n')
			tra_tmp_loop = copy.deepcopy(tra_tmp)
			sum_tra = synthesize(tra_tmp_loop, grid)
			append_sum(sum_tra)
			point_cnt = first_id = 0
			count -= 1
			continue

	write_file(writepath, new_tra)