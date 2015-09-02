#!/usr/bin/env python

import numpy as np
from noise import pnoise2

class Map(object):
    """
    generates and holds a 2D grid of height values, using perlin noise
    """
    
    def __init__(self, width, height, max_depth):
        self.width = width
        self.height = height
        self.max_depth = max_depth
        
        self.heights = [[int(np.ceil(pnoise2(x, y, base=1)*max_depth)) for x in self.__frange(0.0, 1.0, 1.0/width)] for y in self.__frange(0.0, 1.0, 1.0/height)]
        
    def __frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step
            
    def reset(self):
        self.heights = [[int(np.ceil(pnoise2(x, y, base=1)*self.max_depth)) for x in self.__frange(0.0, 1.0, 1.0/self.width)] for y in self.__frange(0.0, 1.0, 1.0/self.height)]
        
if __name__ == '__main__':
    print help(Map)