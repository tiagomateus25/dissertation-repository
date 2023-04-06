#!/usr/bin/env python3
import torch
import numpy as np

# initializing a tensor -------------------------------------------------------------------------------------
# directly from data
data = [[1, 2],[3, 4]]
x_data = torch.tensor(data)

#print(data)
#print(x_data)

# from a numpy array
np_array = np.array(data)
x_np = torch.from_numpy(np_array)

#print(np_array)
#print(x_np)

# from another tensor
x_ones = torch.ones_like(x_data) # retains the properties of x_data
#print(f"Ones Tensor: \n {x_ones} \n")
x_rand = torch.rand_like(x_data, dtype=torch.float) # overrides the datatype of x_data
#print(f"Random Tensor: \n {x_rand} \n")

# with random or constant values

shape = (2,3,)
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape)
zeros_tensor = torch.zeros(shape)

#print(f"Random Tensor: \n {rand_tensor} \n")
#print(f"Ones Tensor: \n {ones_tensor} \n")
#print(f"Zeros Tensor: \n {zeros_tensor}")

# attributes of a tensor ------------------------------------------------------------------------------------

tensor = torch.rand(3,4)


print(f"Shape of tensor: {tensor.shape}")   # shape of tensor
print(f"Datatype of tensor: {tensor.dtype}")    # datatype of tensor
print(f"Device tensor is stored on: {tensor.device}")   # device tensor is stored on

# operation on tensors --------------------------------------------------------------------------------------

# We move our tensor to the GPU if available
if torch.cuda.is_available():
    tensor = tensor.to("cuda")

# standard numpy-like indexing and slicing

tensor = torch.ones(4, 4)
#print(f"First row: {tensor[0]}")
#print(f"First column: {tensor[:, 0]}")
#print(f"Last column: {tensor[..., -1]}")
tensor[:,1] = 0
#print(tensor)

# joining tensors

t1 = torch.cat([tensor, tensor, tensor], dim=1)
#print(t1)

# arithmetic operations 

# This computes the matrix multiplication between two tensors. y1, y2, y3 will have the same value
# ``tensor.T`` returns the transpose of a tensor
y1 = tensor @ tensor.T
y2 = tensor.matmul(tensor.T)

y3 = torch.rand_like(y1)
torch.matmul(tensor, tensor.T, out=y3)

# This computes the element-wise product. z1, z2, z3 will have the same value
z1 = tensor * tensor
z2 = tensor.mul(tensor)

z3 = torch.rand_like(tensor)
torch.mul(tensor, tensor, out=z3)

# single-element tensors

agg = tensor.sum()
agg_item = agg.item()
print(agg_item, type(agg_item))

# in-place operations

print(f"{tensor} \n")
tensor.add_(5)
print(tensor)

# bridge with numpy -----------------------------------------------------------------------------------------
# tensor do numpy array

t = torch.ones(5)
print(f"t: {t}")
n = t.numpy()
print(f"n: {n}")

t.add_(1)
print(f"t: {t}")
print(f"n: {n}")

# numpy array to tensor
n = np.ones(5)
t = torch.from_numpy(n)
np.add(n, 1, out=n)
print(f"t: {t}")
print(f"n: {n}")