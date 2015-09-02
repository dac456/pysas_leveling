#!/usr/bin/env python

import numpy as np
from collections import deque

class Agent(object):
    """
    class representing a single simple agent in the swarm
    contains various properties and variables as well as several uility methods
    """
    
    #TODO: should these be properties or just regular methods?
    @property
    def mem_capacity(self):
        return 8
    
    @property
    def chromosome_length(self):
        return 20
    
    def __init__(self):
        self.idx = (0, 0, 0) # map index/position
        
        self.carrying = False # whether the agent is carrying a unit or not
        self.climbing = False # whether the agent is climbing a gradient
        self.read = True # whether the agent is in the read state or not
        self.halt = False # whether the agent should halt
        
        self.height = 0 # the current sensed height of the agent
        self.last_height = 0 # the last sensed height of the agent
        
        self.direction_i = 1 # vertical map direction
        self.direction_j = 0 # horizontal map direction
        self.facing = 0 # facing direction, 0=N, 1=NE, 2=E, etc...
        
        self.heights = deque(maxlen=self.mem_capacity) # sampled heights
        
        self.chromosome = [([-1 for i in range(self.chromosome_length)],0.0)] # list of GA chromosome/fitness tuples
        self.chromosome_idx = 0 # active chromosome
        
        self.pu_height = -1 # height of last pickup
        self.de_height = -1 # height of last deposit
        self.num_positive = 0 # number of postive changes made for current chromosome
        self.num_positive_tracking = 0 # number of positive changes made for current run
        self.num_pu = 0 # number of successful pickups
        self.num_de = 0 # number of successful deposits
        self.num_pu_attempt = 0 # number of attempted pickups 
        self.num_de_attempt = 0 # number of attempted deposits
        
        self.fitness_function = 0 # selected fitness function
        
    def average(self):
        """
        returns the average of sensed heights
        """
        
        return np.mean(self.heights)    
        
    def max_sensed(self):
        """
        returns maximum value of sensed heights
        """
        
        return max(self.heights)
    
    def fitness(self):
        """
        returns the fitness value for the active GA chromosome
        """
        
        total_attempts = self.num_pu_attempt + self.num_de_attempt
        if total_attempts != 0:
            return self.num_positive/float(total_attempts)
        else:
            return 0.0
        
if __name__ == '__main__':
    print help(Agent)
    
    a = Agent()