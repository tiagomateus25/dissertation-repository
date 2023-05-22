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

        # amplitude
        self.amplitude = 2

        # truncation
        self.steps = 0
        self.max_episode_steps = 20

        # low states
        low = np.array(
            [
                self.init_freq,
                self.amplitude,
                0
            ],
            dtype=np.float32,
        )
        
        # high states
        high = np.array(
            [
                self.last_freq,
                6,
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
        self.x = np.array([])
        self.y = np.array([])

    def reset(self):
        # reset state
        self.state = np.array([self.init_freq, self.amplitude, 0], dtype=np.float32)

        # return reset state
        return np.array(self.state, dtype=np.float32)
    
    def step(self, action):
        # set current state
        self.current_state = self.state
        
        # calculate energy
        Energy = eng.energy(self.current_state, action+1)
        self.state = np.array([self.init_freq, self.amplitude, Energy], dtype=np.float32)

        # rendering
        if self.render_mode == 'human':
            self.render()

        # check terminal condition and calculate reward
        if self.state[2] < self.current_state[2]:
            reward = -100
            terminated = True
        else:
            reward = 1
            terminated = False

        # check if truncated
        self.steps += 1
        truncated = self.steps >= self.max_episode_steps

        # reset steps if terminated or truncated
        done = terminated or truncated
        if done:
            self.steps = 0

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
            self.x = np.append(self.x, self.steps)

            # y axis: average power
            self.y = np.append(self.y, self.state[1])
            
    def close(self):
        # plot results
        self.fig = plt.figure(2)
        plt.scatter(self.x, self.y)
        plt.plot(self.x, self.y)
        plt.xlabel('Steps')
        plt.ylabel('Energy (J)')
        plt.title('Energy per step')
        self.fig.savefig('results_plot.png')


# test env
# env = simple_1DOF_env(render_mode='human')
# episodes = 5
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
#     print('Elapsed time:', end - start, 'seconds.')
#     if env.render_mode == 'human':
#         env.close()
#         if episode != episodes:
#             plt.close()
#         else:
#             env.fig.savefig('plot.png')

