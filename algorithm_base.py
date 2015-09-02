#!/usr/bin/env/ python

import numpy as np

class AlgorithmBase(object):
    
    def __init__(self, grid, params):
        self.grid = grid
        self.params = params
        
    def sense(self, agent):
        agent.last_height = agent.height
        agent.height = self.grid[agent.idx[0]][agent.idx[1]]
        
        r = np.random.ranf()
        if r < self.params['sense_prob']:
            agent.heights.append(self.grid[agent.idx[0]][agent.idx[1]])
            
        agent.climbing = agent.height > agent.last_height
        
    def pickup(self, agent):
        pass
        
    def deposit(self, agent):
        pass
        
    def move_forward(self, agent):
        pass
       
    def move_random(self, agent):
        pass
        
    def rotate_left(self, agent):
        pass
        
    def rotate_right(self, agent):
        pass
        
    def act(self, agent):
        raise NotImplementedError, "Err: must override act() for each algorithm subclass"
            