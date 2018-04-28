import sys
import numpy as np
from environment import Environment

e = Environment(sys.argv[1])

maze_width = e.width
maze_height = e.height
maze = e.maze

qsa = np.zeros(shape=(maze_width*maze_height, 4))

num_episodes = int(sys.argv[5])

max_episode_length = int(sys.argv[6])

learning_rate = float(sys.argv[7])

discount_rate = float(sys.argv[8])

epsilon = float(sys.argv[9])

for epi in xrange(0, 10):

    e.reset()
    curstate = e.state
    #print "epi", epi

    for steps in xrange(0, max_episode_length):

        choose = np.random.uniform(0, 1)

        if epsilon != float(0.0) and choose < epsilon:
            action = np.random.random_integers(0, 3)
        else:
            index = curstate[0] * maze_width + curstate[1]
            action = 0
            max_q_s_a = qsa[index][0]
            for a in xrange(1, 4):
                if qsa[index][a] > max_q_s_a:
                    action = a
                    max_q_s_a = qsa[index][a]

        #print "i", curstate[0], curstate[1], action

        next_step = e.step(action)

        s_index = (next_step[0][0] * maze_width) + next_step[0][1]
        max_q_sp_ap = max(qsa[s_index][0], qsa[s_index][1], qsa[s_index][2], qsa[s_index][3])

        #print "n", next_step[0][0], next_step[0][1]

        qsa[index][action] = ((1 - learning_rate) * qsa[index][action]) \
                             + (learning_rate * (next_step[1] + (discount_rate * max_q_sp_ap)))

        #print "q", index, action, qsa[index][action]

        if next_step[2] == 1:
            break

        curstate = next_step[0]


print qsa

vs = np.zeros(shape=(maze_height, maze_width))
pi = np.zeros(shape=(maze_height, maze_width))

vfile = open(sys.argv[2], "w")
qfile = open(sys.argv[3], "w")
pifile = open(sys.argv[4],"w")

for i in xrange(0, maze_height):
    for j in xrange(0, maze_width):
        if maze[i][j] == 0:
            continue
        index = i * maze_width + j
        max_v = qsa[index][0]
        max_a = 0
        for a in xrange(0, 4):
            if qsa[index][a] > max_v:
                max_v = qsa[index][a]
                max_a = a
            qfile.writelines(str(i) + " " + str(j) + " " + str(qsa[index][a]) + "\n")
        vs[i][j] = max_v
        vfile.writelines(str(i) + " " + str(j) + " " + str(round(vs[i][j], 1)) + "\n")
        pi[i][j] = max_a
        pifile.writelines(str(i) + " " + str(j) + " " + str(round(pi[i][j], 1)) + "\n")

vfile.close()
qfile.close()
pifile.close()
