#!/usr/bin/env python3
import gymnasium as gym
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import matlab.engine
from typing import Optional
import time
import matplotlib.pyplot as plt

eng = matlab.engine.start_matlab()

class simple_1DOF_env(Env):
    def __init__(self, render_mode: Optional[str] = None):

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

        # render
        self.render_mode = render_mode
        self.x = []
        self.y = []

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

        # rendering
        if self.render_mode == 'human':
            self.render()

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
       
    def render(self):
        if self.render_mode is None:
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym("{self.spec.id}", render_mode="rgb_array")'
            )
            return
        
        if self.render_mode == 'human':
            
            # x axis: step
            self.x.append(self.steps)

            # y axis: average power
            self.y.append(self.state[1])
            
    def close(self):
        # check values
        # print(self.x)
        # print(self.y)

        # plot results
        plt.plot(self.x, self.y, 'b-')
        self.x = []
        self.y = []
    

# test env

env = simple_1DOF_env(render_mode='human')

episodes = 5
for episode in range(1, episodes+1):
    state = env.reset()
    terminated = False
    truncated = False
    score = 0
    steps = 0
    start = time.time()
    while not terminated and not truncated:
        action = env.action_space.sample()
        n_state, reward, terminated, truncated, info = env.step(action)
        score += reward
        steps+= 1
    print('Episode:{} Score:{}'.format(episode, score))
    print('Number of steps:', steps)
    end = time.time()
    print('Elapsed time is', end - start, 'seconds.')
    env.close()
    if episode != episodes:
        plt.close()
    plt.show()

