#!/usr/bin/env python3
import os
import gymnasium as gym
from stable_baselines3 import ppo
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy


env = gym.make("CartPole-v1", render_mode="human")

episodes = 5
for episode in range(1, episodes+1):
    state = env.reset()
    done = False
    truncated = False
    score = 0

    while not done or truncated:
        action = env.action_space.sample()
        n_state, reward, done, truncated, info = env.step(action)
        score += reward
    # print(n_state, reward, done, truncated, info)
    # print('Episode:{} Score:{}'.format(episode, score))
env.close()