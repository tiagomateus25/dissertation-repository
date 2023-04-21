#!/usr/bin/env python3

# import gym stuff
import gymnasium as gym
from gym import Env
from gym.spaces import Discrete, Box
# import helpers
import numpy as np
import random
import os


class env(Env):
    def __init__(self):

        high = 1
        low = -high

        # four actions: 0 - open coils, 1 - close coils, 2 - invert coil's polarity, 3 - do nothing
        # self.action_space = Discrete(4)
        self.action_space = Discrete(3)
        
        self._action_to_voltage = {
            0: 0,
            #1: np.array([random.randint(-10,10)]).astype(float),
            1: -1,
            2: 1,
        }

        # observation space: is it the induced potential difference, the measured external vibration or the magnet's position???
        self.observation_space = Box(low=np.array([low]), high=np.array([high]), dtype=np.float32)

    def reset(self):

        # the initial measurement of the induced potential difference
        self.initial_state = np.array([random.randint(-1,1)]).astype(float)

        return np.array(self.initial_state, dtype=np.float32)
    
    def step(self, action):

        # choose an action
        voltage = self._action_to_voltage[action]
        self.state = self.initial_state * voltage

        # reward process
        if self.state > self.initial_state and self.state > 0:
            reward = 10
            terminated = True
        elif self.state == self.initial_state and self.state > 0: # keep positive induced voltage
            reward = 10
            terminated = True
        elif self.state > self.initial_state and self.state == 0:
            reward = 5
            terminated = True
        elif self.initial_state == 0:
            reward = 0
            terminated = True
        else:
            reward = -10
            terminated = True

        # info
        info = {}
        
        return np.array(self.state, dtype=np.float32), reward, terminated, info
    
    def render():
        pass

    def close(self):
        pass


# # test env   
# env = env()
# print(env.observation_space.sample())
# print(env.action_space.sample())

# episodes = 100
# for episode in range(1, episodes+1):
#     state = env.reset()
#     terminated = False
#     truncated = False
#     score = 0

#     while not terminated or truncated:
#         action = env.action_space.sample()
#         n_state, reward, terminated, info = env.step(action)
#         score += reward
#     print('Episode:{} Score:{}'.format(episode, score))
# env.close()

