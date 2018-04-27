import sys
import numpy as np


class Environment:

    def __init__(self, filename):
        mazefile = open(filename, "r")
        row = 0
        col = 0
        for line in mazefile.readlines():
            row = row + 1
            if row == 1:
                for char in line.rstrip():
                    col = col + 1

        self.maze = np.zeros(shape=(row, col))

        self.width = col
        self.height = row
        self.state = [self.height - 1, 0]

        mazefile.seek(0)
        row = 0
        for line in mazefile.readlines():
            col = 0
            for element in line.rstrip():

                if element == "S":
                    self.maze[row][col] = int(2)
                elif element == "G":
                    self.maze[row][col] = int(3)
                elif element == ".":
                    self.maze[row][col] = int(1)
                elif element == "*":
                    self.maze[row][col] = int(0)
                col = col + 1
            row = row + 1
        mazefile.close()
        print self.maze

    def step(self, a):
        next_state = [-1, -1]
        if a == 0:
            next_state[0] = self.state[0]
            if self.state[1] == 0:
                next_state[1] = 0
            else:
                next_state[1] = self.state[1] - 1
                if self.maze[next_state[0]][next_state[1]] == 0:
                    next_state[1] = self.state[1]
        elif a == 1:
            next_state[1] = self.state[1]
            if self.state[0] == 0:
                next_state[0] = 0
            else:
                next_state[0] = self.state[0] - 1
                if self.maze[next_state[0]][next_state[1]] == 0:
                    next_state[0] = self.state[0]
        elif a == 2:
            next_state[0] = self.state[0]
            if self.state[1] == self.width - 1:
                next_state[1] = self.width - 1
            else:
                next_state[1] = self.state[1] + 1
                if self.maze[next_state[0]][next_state[1]] == 0:
                    next_state[1] = self.state[1]
        elif a == 3:
            next_state[1] = self.state[1]
            if self.state[0] == self.height - 1:
                next_state[0] = self.height - 1
            else:
                next_state[0] = self.state[0] + 1
                if self.maze[next_state[0]][next_state[1]] == 0:
                    next_state[0] = self.state[0]

        self.state = next_state

        #if (next_state[0] == self.state[0]) and (next_state[1] == self.state[1]):
            #reward = 0
        #else:
            #reward = -1

        if self.maze[self.state[0], self.state[1]] == 3:
            is_terminal = 1
        else:
            is_terminal = 0

        return [self.state, -1, is_terminal]

    def reset(self):
        self.state = [self.height - 1, 0]

    def writefile(self, seqfilename, outfilename):
        seqfile = open(seqfilename, "r")
        outfile = open(outfilename, "w")
        line = seqfile.read()
        actions = line.split(" ")
        for action in actions:
            ret = self.step(int(action))
            outfile.write(str(ret[0][0]) + " " + str(ret[0][1]) + " " + str(ret[1]) + " " + str(ret[2]) + "\n")
        outfile.close()
        seqfile.close()


#e = Environment(sys.argv[1])
#e.writefile(sys.argv[3], sys.argv[2])
#e.reset()