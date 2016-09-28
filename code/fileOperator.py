__all__ = [
    'count_tra',
    'read_file',
    'write_file',
]

count_tra = 1


def read_file(filepath):
    global count_tra
    maxtrix = [[]]
    count = 0

    file_in = open(filepath, 'r')
    print("Begin read trajectory file...")
    line = file_in.readline().strip().split(' ')
    first = line

    maxtrix[count].append(line)

    while len(line) > 2:
        line = file_in.readline().strip().split(' ')
        if first[0] == line[0]:
            maxtrix[count].append(line)
        else:
            count += 1
            maxtrix.append([])
            first = line
            maxtrix[count].append(line)
            count_tra += 1
            if count_tra > 5000:
                count_tra -= 1
                maxtrix.pop()
                break

    file_in.close()
    print("End read trajectory file...")
    return maxtrix


def write_file(filepath, tra):
    global count_tra
    file_out = open(filepath, 'w')

    for i in range(count_tra):
        for line in tra[i]:
            tmp += ' '.join(line) + '\n'
            file_out.write(tmp)
            
    file_out.close()


def test():
	return 0


if __name__ == "__main__":
	test();