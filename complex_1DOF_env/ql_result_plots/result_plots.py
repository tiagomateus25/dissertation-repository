#!/usr/bin/env python3
import numpy as np
import pickle
import matplotlib.pyplot as plt

with open('amplitude_5.pkl', 'rb') as file:
    a5 = pickle.load(file)

with open('amplitude_10.pkl', 'rb') as file:
    a10 = pickle.load(file)

with open('amplitude_15.pkl', 'rb') as file:
    a15 = pickle.load(file)

with open('amplitude_20.pkl', 'rb') as file:
    a20 = pickle.load(file)


# plot results
fig = plt.figure()

# scatter
plt.scatter(a20[0], a20[1], c='red')
plt.scatter(a15[0], a15[1], c='green')
plt.scatter(a10[0], a10[1], c='orange')
plt.scatter(a5[0], a5[1], c='blue')

# plot
plt.plot(a20[0], a20[1], c='red')
plt.plot(a15[0], a15[1], c='green')
plt.plot(a10[0], a10[1], c='orange')
plt.plot(a5[0], a5[1], c='blue')

plt.xlabel('Frequency')
plt.ylabel('Energy (J)')
plt.title('Energy per step')
plt.legend(["Amplitude: 20 mm", "Amplitude: 15 mm", "Amplitude: 10 mm", "Amplitude: 5 mm"])
# plt.show()
fig.savefig('results_plot.png')