#!/usr/bin/env python3

# import gym stuff
import gymnasium as gym
from gym import Env
from gym.spaces import Discrete, Box

# import helpers
import numpy as np
import random
import os

class myEnv(Env):
    def __init__(self):
        high = 10
        low = -high

        # four actions: 0 - open coils, 1 - invert coil's polarity, 2 - do nothing
        self.action_space = Discrete(3)
        
        self._action_to_voltage = {
            0: 0,
            #1: np.array([random.randint(-10,10)]).astype(float),
            1: -1,
            2: 1,
        }

        # observation space: is it the induced potential difference, the measured external vibration or the magnet's position???
        self.observation_space = Box(low=np.array([low]), high=np.array([high]), dtype=np.float32)

        # state: potential difference
        self.state = np.array([random.randint(-10,10)]).astype(float)

    def reset(self):
        self.initial_state = np.array([random.randint(-10,10)]).astype(float)    # the initial measurement of the induced potential difference
        return np.array(self.state, dtype=np.float32), {}

    def step(self, action):
        voltage = self._action_to_voltage[action]
        self.state = self.initial_state * voltage

        if self.state > self.initial_state:
            reward = 1
            done = False
        else:
            reward = -1
            done = True

        info = {}
    
        # return np.array(self.state, dtype=np.float32), reward, done, False, {}
        return np.array(self.state, dtype=np.float32), reward, done, info
    
    def render():
        pass

    def close(self):
        pass

    
env = myEnv()
# print(env.action_space.sample())
# print(env.observation_space.sample())
# print(env._action_to_voltage)

episodes = 20
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score:{}'.format(episode, score))
env.close()