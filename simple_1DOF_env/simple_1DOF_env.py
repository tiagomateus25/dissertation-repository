#!/usr/bin/env python3
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import matlab.engine
import time

eng = matlab.engine.start_matlab()

class simple_1DOF_env(Env):
    def __init__(self):

        # frequencies
        self.init_freq = 1
        self.last_freq = 6

        # truncation
        self.steps = 0
        self.max_episode_steps = 1000

        # low states
        low = np.array(
            [
                self.init_freq,
                0
            ],
            dtype=np.float32,
        )
        
        # high states
        high = np.array(
            [
                self.last_freq,
                100
            ],
            dtype=np.float32,
        )

        # action space
        self.action_space = Discrete(8)

        # observation space
        self.observation_space = Box(low, high, dtype=np.float32)

    def reset(self):
        # reset state
        self.state = np.array([self.init_freq, 0], dtype=np.float32)

        # return reset state
        return np.array(self.state, dtype=np.float32)
    
    def step(self, action):
        # set current state
        self.current_state = self.state
        
        # calculate average power
        AveragePower = eng.avPow(self.current_state[0], action+1)
        self.state = np.array([self.init_freq, AveragePower], dtype=np.float32)

        # check if truncated
        self.steps += 1
        truncated = self.steps >= self.max_episode_steps

        # check terminal condition and calculate reward
        if self.state[1] < self.current_state[1]:
            reward = -10
            terminated = True
            self.steps = 0
        else:
            reward = 1
            terminated = False

        # info 
        info = {}

        # return
        return np.array(self.state, dtype=np.float32), reward, terminated, truncated, info
       
    def render():
        pass

    def close(self):
        pass


# test env

# env = simple_1DOF_env()

# episodes = 1
# for episode in range(1, episodes+1):
#     state = env.reset()
#     terminated = False
#     truncated = False
#     score = 0
#     steps = 0
#     start = time.time()
#     while not terminated and not truncated:
#         action = env.action_space.sample()
#         n_state, reward, terminated, truncated, info = env.step(action)
#         score += reward
#         steps+= 1
#     print('Episode:{} Score:{}'.format(episode, score))
#     print('Number of steps:', steps)
#     end = time.time()
#     print('Elapsed time is', end - start, 'seconds.')
# env.close()

