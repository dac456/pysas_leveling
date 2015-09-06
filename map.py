#!/usr/bin/env python

import numpy as np
from noise import pnoise3

class Map(object):
    """
    generates and holds a 2D grid of height values, using perlin noise
    """
    
    def __init__(self, width, height, max_depth, params, seed=1):
        self.width = width
        self.height = height
        self.max_depth = max_depth
        self.params = params
        
        self.z = np.random.randint(0,65535)
        self.seed = seed
        self.reset(seed)
        
    def __frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step
            
    def __total_volume(self, grid):
        s = 0
        for y in range(self.height):
            s += sum(grid[y])
            
        return s
        
    def __make_optimal(self):
        target = self.__total_volume(self.heights)
        
        i = j = 0
        while target > self.__total_volume(self.optimal_heights):
            self.optimal_heights[j][i] += 1
            
            j += 1
            if(j == self.height):
                j = 0
                i = (i + 1) % self.width
                
    def __grid_max(self, grid):
        rows = []
        for y in range(self.height):
            rows.append(max(grid[y]))
 
        return max(rows)
        
    def total_units(self):
        return self.__total_volume(self.heights)
                
    def is_optimal(self):
        out = True
        
        if self.params['oracle_termination'] == True:
            for hy in self.heights:
                for hx in hy:
                    if hx > self.__grid_max(self.optimal_heights):
                        out = False
                        break
                    
        return out
            
    def reset(self, seed):
        self.heights = [[int(np.abs(np.ceil(pnoise3(x, y, self.z, base=seed)*self.max_depth))) for x in self.__frange(0.0, 1.0, 1.0/self.width)] for y in self.__frange(0.0, 1.0, 1.0/self.height)]
        self.optimal_heights = [[0 for x in range(self.width)] for y in range(self.height)]
        self.__make_optimal()
        
if __name__ == '__main__':
    print help(Map)