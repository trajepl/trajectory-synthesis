import grid
import fileOperator


def call_grid(filepath):
    tra = fileOperator.read_file(filepath)

    max_lng, max_lat, min_lng, min_lat = grid.max_range(tra)
    interval = (max(max_lng - min_lng, max_lat - min_lat) / 200)

    grid_ceil, repeat = grid.cluster(tra, min_lng, min_lat, interval)
    return grid_ceil


def get_grid(method, area):
    area = area.lower()
    if "beijing" == area:
        num = call_grid("../resultdata/Beijing/" + method + ".txt")
        num_origin = call_grid("../falsedata/b13k.txt")
    elif "shanghai" == area:
        num = call_grid("../resultdata/Shanghai/" + method + ".txt")
        num_origin = call_grid("../falsedata/s13k.txt")

    return num, num_origin


def diff(num, num_origin):
    sum = 0
    for i in range(200):
        for j in range(200):
            tmp = abs(len(num) / 4977689 - len(num_origin) / 1401413)
            sum = sum + tmp
    print(sum)


if __name__ == "__main__":
    num, num_origin = get_grid("RG", "Beijing")
    # num, num_origin = get_grid("RG", "Shanghai")

    diff(num, num_origin)
