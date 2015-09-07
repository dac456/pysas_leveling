#!/usr/bin/env python

from algorithm_base import *
from stats_logger import *

class AlgorithmStandard(AlgorithmBase):
    
    def __init__(self, grid, params):
        super(AlgorithmStandard, self).__init__(grid, params)
        
    def pickup_ok(self, agent):
        r = np.random.ranf()
        return (agent.carrying == False and agent.height > agent.average() and agent.height > 0 and r < self.params['act_prob'])
        
    def deposit_ok(self, agent):
        r = np.random.ranf()
        return (agent.carrying == True and agent.height < agent.average() and r < self.params['act_prob'])
        
    def __read(self, agent):
        self.sense(agent)
    
    def __write(self, agent):
        if self.pickup_ok(agent):
            self.pickup(agent)
        elif self.deposit_ok(agent):
            self.deposit(agent)
            
        r = np.random.ranf()
        if r < 0.75:
            if np.abs(np.random.randint(0,65535)) % 2 == 0:
                if self.params['follow_gradient']:
                    if not agent.climbing:
                        self.rotate_left(agent)
                else:
                    self.rotate_left(agent)
            elif np.abs(np.random.randint(0,65535)) % 2 == 1:
                if self.params['follow_gradient']:
                    if not agent.climbing:
                        self.rotate_right(agent)
                else:
                    self.rotate_right(agent)
                
        self.move_forward(agent)
        
    def act_impl(self, agent):
        if agent.halt == False:        
            if agent.read:
                self.__read(agent)
                agent.read = False
            else:
                self.__write(agent)
                agent.read = True
                
    def reset_impl(self):
        pass