import numpy as np

arr = np.array([[[1,2,3],[2,3,4],[3,4,5]],
                [[1,2,3],[2,3,4],[3,4,5]]])
print(arr)
arr = np.flip(arr,axis=1)
print(arr)

print("test")
array = np.array([[[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]],
                  [[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]]])

# 指定した軸に対して反転する
print(array)
flipped_array = np.flip(array, axis=1)

print(flipped_array)