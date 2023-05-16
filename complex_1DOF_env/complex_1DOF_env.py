#!/usr/bin/env python3
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import matlab.engine
import time

eng = matlab.engine.start_matlab()

class complex_1DOF_env(Env):
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
                0,
                0,
            ],
            dtype=np.float32,
        )
        
        # high states
        high = np.array(
            [
                self.last_freq,
                100,
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
        self.state = np.array([self.init_freq, 0, 0], dtype=np.float32)

        # return reset state
        return np.array(self.state, dtype=np.float32)
    
    def step(self, action):
        # set current state
        self.current_state = self.state
        
        # calculate average power
        AveragePower = eng.avPow(self.current_state, action+1)

        # calculate next frequency
        new_freq = self.current_state[0] + 1

        # sum average power
        total_AvPow = self.current_state[1] + AveragePower

        # check terminal condition and calculate reward
        if new_freq == self.last_freq:
            self.state = np.array([self.init_freq, 0, total_AvPow], dtype=np.float32)
            if  self.state[2] < self.current_state[2]:
                reward = -10
                terminated = True
                self.steps = 0
            else:
                reward = 1
                terminated = False
        else:
            self.state = np.array([new_freq, total_AvPow, self.current_state[2]], dtype=np.float32)
            terminated = False
            reward = 0
        # info 
        info = {}
        
        # check if truncated
        self.steps += 1
        truncated = self.steps >= self.max_episode_steps

        # return
        return np.array(self.state, dtype=np.float32), reward, terminated, truncated, info
       
    def render():
        pass

    def close(self):
        pass


# test env

# env = complex_1DOF_env()

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

