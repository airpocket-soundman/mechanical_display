import numpy as np

arr = np.array([[[1,2,3],[2,3,4],[3,4,5]],[[1,2,3],[2,3,4],[3,4,5]]])
print(arr)
arr = np.transpose(arr, axes=(0, 2, 1))[:, ::-1, :]
print(arr)
arr = np.transpose(arr, axes=(0, 2, 1))[:, ::-1, :]
print(arr)
arr = np.transpose(arr, axes=(0, 2, 1))[:, ::-1, :]
print(arr)