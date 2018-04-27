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




print qsa[0][0]
print qsa[0][1]
print qsa[0][2]
print qsa[0][3]
print qsa[1][0]
print qsa[1][1]
print qsa[1][2]
print qsa[1][3]
print qsa[2][0]
print qsa[2][1]
print qsa[2][2]
print qsa[2][3]
print qsa[3][0]
print qsa[3][1]
print qsa[3][2]
print qsa[3][3]











