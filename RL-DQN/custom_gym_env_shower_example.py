#!/usr/bin/env python3

# import gym stuff
import gymnasium as gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple,MultiBinary, MultiDiscrete

# import helpers
import numpy as np
import random
import os 


class ShowerEnv(Env):
    def __init__(self):
        self.action_space = Discrete(3)
        self.observation_space = Box(low=np.array([0]), high=np.array([100]), shape=(1,), dtype=np.float32)
        self.state = 38 + random.randint(-3, 3)
        self.shower_length = 60
        
    def step(self, action):
        # apply temperature adjustment
        self.state += action - 1
        # decrease shower time
        self.shower_length -= 1
        # calculate reward
        if self.state >= 37 and self.state <= 39:
            reward = 1
        else:
            reward = -1
        if self.shower_length <= 0:
            done = True
        else:
            done = False

        info = {}

        # return self.state, reward, done, info
        return np.array(self.state, dtype=np.float32), reward, done, False
    def render(self):
        # implement visualization
        pass
    def reset(self):
        self.state = np.array([38+random.randint(-3,3)]).astype(float)
        self.shower_length = 60
        # return self.state
        return np.array(self.state, dtype=np.float32), {}

env = ShowerEnv()
print(env.observation_space.sample())
print(env.action_space.sample())

episodes = 5
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    truncated = False
    score = 0

    while not done or truncated:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode, score))
env.close()