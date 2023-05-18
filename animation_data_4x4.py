import numpy as np

class animationData():
    def __init__(self):
        self.RightLow2LeftUp = np.array([[[0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0]],
                                         [[0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,7]],
                                         [[0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,7],
                                          [0,0,7,6]],
                                         [[0,0,0,0],
                                          [0,0,0,7],
                                          [0,0,7,6],
                                          [0,7,6,0]],
                                         [[0,0,0,7],
                                          [0,0,7,6],
                                          [0,7,6,5],
                                          [7,6,5,4]],
                                         [[0,0,7,6],
                                          [0,7,6,5],
                                          [7,6,5,4],
                                          [6,5,4,3]],
                                         [[0,7,6,5],
                                          [7,6,5,4],
                                          [6,5,4,3],
                                          [5,4,3,2]],
                                         [[7,6,5,4],
                                          [6,5,4,3],
                                          [5,4,3,2],
                                          [4,3,2,1]],
                                         [[6,5,4,3],
                                          [5,4,3,2],
                                          [4,3,2,1],
                                          [3,2,1,0]],
                                         [[5,4,3,2],
                                          [4,3,2,1],
                                          [3,2,1,0],
                                          [2,1,0,0]],
                                         [[4,3,2,1],
                                          [3,2,1,0],
                                          [2,1,0,0],
                                          [1,0,0,0]],
                                         [[3,2,1,0],
                                          [2,1,0,0],
                                          [1,0,0,0],
                                          [0,0,0,0]],
                                         [[2,1,0,0],
                                          [1,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0]],
                                         [[1,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0]],
                                         [[0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0],
                                          [0,0,0,0]]])
        
        self.LeftLow2RightUp = np.transpose(self.RightLow2LeftUp, axes=(0, 2, 1))[:, ::-1, :]
        self.LeftUp2RightLow = np.transpose(self.LeftLow2RightUp, axes=(0, 2, 1))[:, ::-1, :]  
        self.RightUp2LeftLow = np.transpose(self.LeftUp2RightLow, axes=(0, 2, 1))[:, ::-1, :]

        self.RightLow2LeftUp = self.RightLow2LeftUp * (2**5)
        self.RightUp2LeftLow = self.RightUp2LeftLow * (2**5)
        self.LeftLow2RightUp = self.LeftLow2RightUp * (2**5)
        self.LeftUp2RightLow = self.LeftUp2RightLow * (2**5)

    def animeDataTest(self):
        print(self.RightLow2LeftUp)