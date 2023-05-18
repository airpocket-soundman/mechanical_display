import numpy as np

 
def invert(dotImage):
    dotImage = 255 - dotImage
    return dotImage
    
def hflip(dotImage):
    dotImage = np.flip(dotImage, axis=1)
    return dotImage

def vflip(dotImage):
    dotImage = np.flip(dotImage, axis=2)
    return dotImage

def rotate90(dotImage):
    dotImage = np.rot90(dotImage, axes=(1, 2))
    return dotImage

def rotate180(dotImage):
    dotImage = np.rot90(dotImage, axes=(1, 2), k=2)
    return dotImage

def rotate270(dotImage):
    dotImage = np.rot90(dotImage, axes=(1, 2), k=3)
    return dotImage