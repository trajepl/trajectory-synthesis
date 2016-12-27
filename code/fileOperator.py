__all__ = [
    'count_tra',
    'read_file',
    'write_file',
]

count_tra = 1


def read_file(filepath):
    global count_tra
    matrix = [[]]
    count = 0

    file_in = open(filepath, 'r')
    print("Begin read trajectory file...")
    line = file_in.readline().strip().split(' ')
    first = line

    matrix[count].append(line)

    while len(line) > 2:
        line = file_in.readline().strip().split(' ')
        if first[0] == line[0]:
            matrix[count].append(line)
        else:
            count += 1
            matrix.append([])
            first = line
            matrix[count].append(line)
            count_tra += 1
            if count_tra > 5000:
                count_tra -= 1
                matrix.pop()
                break

    file_in.close()
    print("End read trajectory file...")
    return matrix


def write_file(filepath, tra):
    file_out = open(filepath, 'w')

    print("Dividing...")
    cnt = 0
    for i in range(len(tra)):
        for line in tra[i]:
            tmp = str(cnt) + " " + line[1] + " " + line[2] + " " + line[3] + "\n"
            file_out.write(tmp)
        cnt += 1

    file_out.close()
    print("Finished...")


def test():
    return 0


if __name__ == "__main__":
    test()
