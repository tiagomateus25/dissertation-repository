#!/usr/bin/env python3
import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# get device for training -----------------------------------------------------------------------------------
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

# define the class ------------------------------------------------------------------------------------------

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork().to(device)  # instance of nn and move it to device
print(model)

X = torch.rand(1, 28, 28, device=device)
logits = model(X)
pred_probab = nn.Softmax(dim=1)(logits)
y_pred = pred_probab.argmax(1)
print(f"Predicted class: {y_pred}")

# model layers ----------------------------------------------------------------------------------------------

input_image = torch.rand(3,28,28)
print(input_image.size())

# nn.flatten converts a 2D 28x28 image into a contiguous array of 784

flatten = nn.Flatten()
flat_image = flatten(input_image)
print(flat_image.size())

# linear layer apples a linear transformation 
layer1 = nn.Linear(in_features=28*28, out_features=20)
hidden1 = layer1(flat_image)
print(hidden1.size())

# non-linear activations are applied after linear transformations to introduce non-linearity ----------------

print(f"Before ReLU: {hidden1}\n\n")
hidden1 = nn.ReLU()(hidden1)
print(f"After ReLU: {hidden1}")

# nn.Sequential is an ordered container of modules
seq_modules = nn.Sequential(
    flatten,
    layer1,
    nn.ReLu(),
    nn.Linear(20,10)
)
input_image = torch.rand(3,28,28)
logits = seq_modules(input_image)

# the last linear transf returns logits -raw values which are passed to the nn.Softmax module.
# the logits are scaled to values [0,1] representing the model's predicted probabilities for each class.
softmax = nn.Softmax(dim=1)
pred_probab = softmax(logits)

# model parameters
print(f"Model structure: {model}\n\n")

for name, param in model.named_parameters():
    print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]} \n")