#!/usr/bin/env python3
import os
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from simple_1DOF_env import simple_1DOF_env

env = simple_1DOF_env()
log_path = os.path.join('Training', 'logs')
model = DQN('MlpPolicy', env, verbose = 1, tensorboard_log=log_path)
model.learn(total_timesteps=50000)