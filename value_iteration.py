import sys
import numpy as np


def get_next_state(state, action):
    next_state = [-1, -1]
    if action == 0:
        next_state[0] = state[0]
        if state[1] == 0:
            next_state[1] = 0
        else:
            next_state[1] = state[1] - 1
            if maze[next_state[0]][next_state[1]] == 0:
                next_state[1] = state[1]
    elif action == 1:
        next_state[1] = state[1]
        if state[0] == 0:
            next_state[0] = 0
        else:
            next_state[0] = state[0] - 1
            if maze[next_state[0]][next_state[1]] == 0:
                next_state[0] = state[0]
    elif action == 2:
        next_state[0] = state[0]
        if state[1] == width - 1:
            next_state[1] = width - 1
        else:
            next_state[1] = state[1] + 1
            if maze[next_state[0]][next_state[1]] == 0:
                next_state[1] = state[1]
    elif action == 3:
        next_state[1] = state[1]
        if state[0] == height - 1:
            next_state[0] = height - 1
        else:
            next_state[0] = state[0] + 1
            if maze[next_state[0]][next_state[1]] == 0:
                next_state[0] = state[0]

    return next_state


mazefile = open(sys.argv[1], "r")
row = 0
col = 0
for line in mazefile.readlines():
    row = row + 1
    if row == 1:
        for char in line.rstrip():
            col = col + 1

width = col
height = row
maze = np.zeros(shape=(height, width))
curstate = [height - 1, 0]

mazefile.seek(0)
row = 0
for line in mazefile.readlines():
    col = 0
    for element in line.rstrip():
        if element == "S":
            maze[row][col] = int(2)
        elif element == "G":
            maze[row][col] = int(3)
        elif element == ".":
            maze[row][col] = int(1)
        elif element == "*":
            maze[row][col] = int(0)
        col = col + 1
    row = row + 1
mazefile.close()

print maze

num_epochs = int(sys.argv[5])
discount_rate = float(sys.argv[6])

vs = [float(0.0)] * (width*height)

for e in xrange(0, num_epochs):
    vs_temp = [0] * (width * height)
    for i in xrange(0, height):
        for j in xrange(0, width):
            if maze[i][j] == 0:
                continue
            qsa = [0] * 4
            if maze[i][j] != 3:
                for a in xrange(0, 4):
                    nextstate = get_next_state([i, j], a)
                    index = nextstate[0] * width + nextstate[1]
                    qsa[a] = float(-1.0) + (discount_rate * vs[index])
                index = i * width + j
                vs_temp[index] = max(qsa)
            else:
                index = i * width + j
                vs_temp[index] = 0
    vs = vs_temp

print vs

vfile = open(sys.argv[2], "w")
qfile = open(sys.argv[3], "w")
pifile = open(sys.argv[4], "w")

for i in xrange(0, height):
    for j in xrange(0, width):
        if maze[i][j] == 0:
            continue
        vfile.writelines(str(i) + " " + str(j) + " "+str(round(vs[i*width+j], 2)) + "\n")

        qsa = [0] * 4
        if maze[i][j] != 3:
            for a in xrange(0, 4):
                nextstate = get_next_state([i, j], a)
                index = nextstate[0] * width + nextstate[1]
                qsa[a] = -1 + (discount_rate * vs[index])
                qfile.writelines(str(i) + " " + str(j) + " " + str(a) + " " +str(round(qsa[a], 2)) + "\n")
        else:
            for a in xrange(0, 4):
                qfile.writelines(str(i) + " " + str(j) + " " + str(a) + " " + str(round(0.0, 2)) + "\n")
        max_qsa = max(qsa)
        pifile.writelines(str(i) + " " + str(j) + " " + str(round(qsa.index(max_qsa), 1)) + "\n")

vfile.close()
qfile.close()
pifile.close()
