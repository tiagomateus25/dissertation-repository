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

class complex_1DOF_env(Env):
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
                0,
                0,
            ],
            dtype=np.float32,
        )
        
        # high states
        high = np.array(
            [
                self.last_freq,
                6,
                100,
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
        self.state = np.array([self.init_freq, self.amplitude, 0, 0], dtype=np.float32)

        # return reset state
        return np.array(self.state, dtype=np.float32)
    
    def step(self, action):
        # set current state
        self.current_state = self.state
        
        # calculate average power
        self.energy = eng.energy(self.current_state, action+1)

        # calculate next frequency
        new_Freq = self.current_state[0] + 1

        # sum average power
        total_Energy = self.current_state[2] + self.energy

        # rendering
        if self.render_mode == 'human':
            self.render()

        # check terminal condition and calculate reward
        if new_Freq == self.last_freq:
            self.state = np.array([self.init_freq, self.amplitude, 0, total_Energy], dtype=np.float32)
            if  self.state[3] < self.current_state[3]:
                reward = -100
                terminated = True
                self.steps = 0
            else:
                reward = 1
                terminated = False
        else:
            self.state = np.array([new_Freq, self.amplitude, total_Energy, self.current_state[3]], dtype=np.float32)
            terminated = False
            reward = 0
        # info 
        info = {}
        
        # check if truncated
        self.steps += 1
        truncated = self.steps >= self.max_episode_steps

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
            self.x = np.append(self.x, self.current_state[0])

            # y axis: energy
            self.y = np.append(self.y, self.energy)

    def close(self):
        # plot results
        self.fig = plt.figure(2)
        plt.scatter(self.x, self.y)
        plt.plot(self.x, self.y)
        plt.xlabel('Frequency')
        plt.ylabel('Energy (J)')
        plt.title('Energy per step')
        self.fig.savefig('results_plot.png')


# test env
env = complex_1DOF_env(render_mode='human')
episodes = 1
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

