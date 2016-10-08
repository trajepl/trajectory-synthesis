import os
import time
import figure

def allInShanghai(tra):
	for point in tra:
		point = point.strip().split(',')
		if not inShanghai(point):
			return False
	return True


def inShanghai(point_tmp):
	min_lng, max_lng = 120.51, 122.12
	min_lat, max_lat = 30.40, 31.53
	
	if len(point_tmp) >= 4:
		if float(point_tmp[0]) > min_lng and float(point_tmp[0]) < max_lng and float(point_tmp[1]) > min_lat and float(point_tmp[1]) < max_lat:
			return True
		else:
			return False
	return False

def readDirData(fileDir, writePath):
	global lng_arr, lat_arr
	files = os.listdir(fileDir)

	file_out = open(writePath, "w")
	tra_cnt = 0
	for file in files:
		print(file)
		file_in = open(fileDir + '/' + file, "r")
		tra = file_in.readline().strip().split(';')[:-1]
		
		
		while len(tra) >= 2:		
			if allInShanghai(tra):
				for point in tra:
					point = point.strip().split(',')
					file_out.write(str(tra_cnt) + " " + point[-2] + " " + point[0] + " " + point[1] + '\n')
					
					lng_arr[tra_cnt].append(float(point[0]))
					lat_arr[tra_cnt].append(float(point[1]))

				tra_cnt += 1
				lng_arr.append([])
				lat_arr.append([])

			tra = file_in.readline().strip().split(';')[:-1]
		print("Finishing the file '" + file + "' read.")
		
		file_in.close()

		if tra_cnt >= 22000:
			file_out.close()
			return 0



if __name__ == "__main__" :
	lng_arr, lat_arr = [[]], [[]]
	fileDir = "D:/BaiduYunDownload/gaotong/d01"
	writePath = "D:/git-repo/trajectory-synthesis/falsedata/s13k.txt"
	readDirData(fileDir, writePath)
	print(lng_arr[1:2], lat_arr[1:2])
	figure.figDensity(lng_arr[1:2], lat_arr[1:2])


