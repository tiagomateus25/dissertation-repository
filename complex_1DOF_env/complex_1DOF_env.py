#!/usr/bin/env python3
import gymnasium as gym
from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import matlab.engine
from typing import Optional
import time
import matplotlib.pyplot as plt
import pickle


eng = matlab.engine.start_matlab()

class complex_1DOF_env(Env):
    def __init__(self, render_mode: Optional[str] = None):

        # frequencies
        self.init_freq = 1
        self.last_freq = 6

        # amplitude
        self.amplitude = 20

        # truncation
        self.steps = 0
        self.max_episode_steps = 120

        # low states
        low = np.array(
            [
                0,                  # frequency (Hz)
                0,                  # amplitude (m/s²)
                0,                  # energy (J)
                0                   # total energy (J)
            ],
            dtype=np.float32,
        )
        
        # high states
        high = np.array(
            [
                7,                  # frequency (Hz)
                21,                 # amplitude (m/s²)
                0.76e-4,            # energy (J)
                0.76e-4             # total energy (J)
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

        # calculate terminal condition, reward and new state
        if self.current_state[0] == self.last_freq:
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
            # error warning
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
        # split and stack data for plotting
        self.x = np.split(self.x, len(self.x)/self.last_freq)
        self.x = np.vstack(self.x)
        self.y = np.split(self.y, len(self.y)/self.last_freq)
        self.y = np.vstack(self.y)

        # save variable in a file
        with open('amplitude_20.pkl', 'wb') as file:
            pickle.dump([self.x.T, self.y.T], file)

        # plot results
        self.fig = plt.figure(2)
        plt.scatter(self.x.T, self.y.T)
        plt.plot(self.x.T, self.y.T)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Energy (J)')
        plt.title('Energy per step')
        self.fig.savefig('results_plot.png')


# test env
# env = complex_1DOF_env(render_mode='human')
# episodes = 3
# for episode in range(1, episodes+1):
#     state = env.reset()
#     terminated = False
#     truncated = False
#     score = 0
#     steps = 0

#     if env.render_mode == 'human':
#         env.x = np.array([])
#         env.y = np.array([])

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

#     # save last plot
#     if env.render_mode == 'human':
#         if episode == episodes:
#             env.close()

# with open('amplitude_5.pkl', 'rb') as file:
#     a = pickle.load(file)
# print(a[1])

# plt.figure(1)
# plt.scatter(a[0], a[1])
# plt.plot(a[0], a[1])
# plt.xlabel('Frequency')
# plt.ylabel('Energy (J)')
# plt.title('Energy per step')
# plt.show()

# ---------------------------------------------------------------------------------------------------

# calculate energy values
# amplitude = np.array([5, 10, 15, 20])
# actions = np.array([1, 2, 3, 4, 5, 6, 7, 8])

# c = np.array([])
# for amp in amplitude:
#     current_state = np.array([[1, amp], [2, amp], [3, amp], [4, amp], [5, amp], [6, amp]])
#     b = np.array([], dtype=np.float32)
#     for i in current_state:
#         a = np.array([], dtype=np.float32)
#         for k in actions:
#             # calculate average power
#             energy = eng.energy(i, actions[k-1])
#             a = np.append(a, energy)
#         max = np.max(a)
#         b = np.append(b, max)
#     sum = np.sum(b)
#     c = np.append(c, sum)

# print(c)
