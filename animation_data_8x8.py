import numpy as np

class animationData():
    def __init__(self):
        self.RightLow2LeftUp = np.array([[[0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,7,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[0,0,0,0,0,0,0,0],
                                          [0,0,0,7,0,0,0,0],
                                          [0,0,7,6,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[0,0,0,0,0,0,0,0],
                                          [0,0,0,7,0,0,0,0],
                                          [0,0,7,6,0,0,0,0],
                                          [0,7,6,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[0,0,0,7,0,0,0,0],
                                          [0,0,7,6,0,0,0,0],
                                          [0,7,6,5,0,0,0,0],
                                          [7,6,5,4,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[0,0,7,6,0,0,0,0],
                                          [0,7,6,5,0,0,0,0],
                                          [7,6,5,4,0,0,0,0],
                                          [6,5,4,3,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[0,7,6,5,0,0,0,0],
                                          [7,6,5,4,0,0,0,0],
                                          [6,5,4,3,0,0,0,0],
                                          [5,4,3,2,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[7,6,5,4,0,0,0,0],
                                          [6,5,4,3,0,0,0,0],
                                          [5,4,3,2,0,0,0,0],
                                          [4,3,2,1,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[6,5,4,3,0,0,0,0],
                                          [5,4,3,2,0,0,0,0],
                                          [4,3,2,1,0,0,0,0],
                                          [3,2,1,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[5,4,3,2,0,0,0,0],
                                          [4,3,2,1,0,0,0,0],
                                          [3,2,1,0,0,0,0,0],
                                          [2,1,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[4,3,2,1,0,0,0,0],
                                          [3,2,1,0,0,0,0,0],
                                          [2,1,0,0,0,0,0,0],
                                          [1,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[3,2,1,0,0,0,0,0],
                                          [2,1,0,0,0,0,0,0],
                                          [1,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[2,1,0,0,0,0,0,0],
                                          [1,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[1,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]],
                                         [[0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0],
                                          [0,0,0,0,0,0,0,0]]])
        
        self.LeftLow2RightUp = np.transpose(self.RightLow2LeftUp, axes=(0, 2, 1))[:, ::-1, :]
        self.LeftUp2RightLow = np.transpose(self.LeftLow2RightUp, axes=(0, 2, 1))[:, ::-1, :]  
        self.RightUp2LeftLow = np.transpose(self.LeftUp2RightLow, axes=(0, 2, 1))[:, ::-1, :]


    def animeDataTest(self):
        print(self.RightLow2LeftUp)