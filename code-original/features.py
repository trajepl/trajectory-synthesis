import math
import figure


def show():
    # path = "../falsedata/13K.txt"
    path = "../resultdata/genTra2.txt"
    global count_tra
    l = [0 for x in range(0, 20)]
    rates = [0 for x in range(0, 20)]
    acc = [0 for x in range(0, 20)]
    ag = [0 for x in range(0, 20)]

    trajectory = read_file(path)
    for i in range(0, len(trajectory)):
        tra_len, tra_rate, tra_ac, tra_turn = features(trajectory[i])
        x = select_length(tra_len)
        y = select_rate(tra_rate)
        z = select_acc(tra_ac)
        m = select_turn(tra_turn)
        if x < 20:
            l[x] += 1
        if y < 20:
            rates[y] += 1
        if z < 20:
            acc[z] += 1
        if m < 20:
            ag[m] += 1

    num_len, num_rate, num_ac, num_turn = map(sum_features, [l, rates, acc, ag])
    # map(rates_features, [l, rates, acc, ag], [num_len, num_rate, num_ac, num_turn])

    for i in range(20):
        l[i] = "%.4f" % (l[i] / num_len)
        rates[i] = " %.4f" % (rates[i] / num_rate)
        acc[i] = "%.4f" % (acc[i] / num_ac)
        ag[i] = "%.4f" % (ag[i] / num_turn)

    figure.fig(l, "length")
    figure.fig(rates, "speed")
    figure.fig(acc, "acceleration")
    figure.fig(ag, "U-turn")


def read_file(filepath):
    traje_file = open(filepath, 'r')
    matrix = []
    matrix.append([])
    global count_tra
    count = 0
    line = traje_file.readline().strip().split(' ')
    first = line

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


def geo_len(lng1, lat1, lng2, lat2):
    r = 6371000
    lng1, lat1, lng2, lat2 = map(math.radians, [lng1, lat1, lng2, lat2])

    cal_lng = lng2 - lng1
    cal_lat = lat2 - lat1

    step1 = math.sin(cal_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(cal_lng / 2) ** 2
    step2 = 2 * math.asin(min(1, math.sqrt(step1)))
    distance = r * step2
    if distance > 1000:
        return 0
    return distance


def sum_features(f):
    sum_f = 0
    for i in f:
        sum_f += i
    return sum_f


def rates_features(f, sum_f):
    for i in f:
        i = i / sum_f


def select_length(num):
    if num > 0:
        return int(float(num) / 1000) // 10
    return 21


def select_rate(num):
    if num > 0:
        return int(num)
    return 21


def select_acc(num):
    if num > 0:
        return int(float(num) * 100)
    return 21


def select_turn(num):
    if num > 0:
        return int(num) // 10
    return 21


def cos_law(a, b, c):
    if b == 0 or c == 0 or a == 0:
        return 0
    return (a ** 2 + b ** 2 - c ** 2) / (2 * b * a)


def toTime(time):
    return int(time[-1]) + int(time[-2]) * 10 + (int(time[-3]) + int(time[-4]) * 10) * 60 + (int(time[-5]) + int(
        time[-6]) * 10) * 3600 + (int(time[-7]) + int(time[-8])) * 24 * 3600


def features(tra):
    sum_len = 0

    sum_rate = 0
    rate = 0

    sum_ac = 0
    ac = 0

    u_turn = 0
    flag_angle = math.cos(math.radians(90))

    if len(tra) >= 2:
        for i in range(1, len(tra)):
            time1 = toTime(tra[i][1])
            time2 = toTime(tra[i - 1][1])
            delta_len_a = geo_len(float(tra[i][3]), float(tra[i][2]), float(tra[i - 1][3]), float(tra[i - 1][2]))

            if len(tra) >= 3 and i + 1 < len(tra):
                time3 = toTime(tra[i + 1][1])

                delta_len_b = geo_len(float(tra[i][3]), float(tra[i][2]), float(tra[i + 1][3]), float(tra[i + 1][2]))
                delta_len_c = geo_len(float(tra[i - 1][3]), float(tra[i - 1][2]), float(tra[i + 1][3]),
                                      float(tra[i + 1][2]))
                if time1 != time2 and time2 != time3 and time1 != time3:
                    rate = abs(delta_len_a / (time1 - time2))
                    rate1 = abs(delta_len_c / (time3 - time1))
                    ac = abs((rate - rate1) / (time3 - time2))

                if cos_law(delta_len_a, delta_len_b, delta_len_c) >= flag_angle:
                    u_turn += 1

            sum_len += delta_len_a
            sum_rate += rate
            sum_ac += ac
        rate = sum_rate / (len(tra) - 1)
        ac = sum_ac / (len(tra) - 1)
    # print('%f\n' %(sum_len))
    return sum_len, rate, ac, u_turn


if __name__ == '__main__':
    show()
