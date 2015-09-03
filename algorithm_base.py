#!/usr/bin/env/ python

import numpy as np
from map import *
from agent import *

class AlgorithmBase(object):
    
    def __init__(self, grid, params):
        self.grid = grid
        self.params = params
        
        # initialize agents
        num_agents = params['num_agents']
        self.agents = [Agent() for i in range(num_agents)]      
        
        # statistics
        self.voxels_moved = 0
        self.num_act_calls = 0
        
    def __is_agent_at_index(x, y):
        for a in self.agents:
            if a.idx[0] == x and a.idx[1] == y:
                return True
                
        return False
        
    def sense(self, agent):
        agent.last_height = agent.height
        agent.height = self.grid[agent.idx[1]][agent.idx[0]]
        
        r = np.random.ranf()
        if r < self.params['sense_prob']:
            agent.heights.append(self.grid[agent.idx[1]][agent.idx[0]])
            
        agent.climbing = agent.height > agent.last_height
        
    def pickup(self, agent, pickup_ok):
        agent.num_pu_attempt += 1
        
        if pickup_ok(agent):
            agent.carrying = True
            agent.pu_height = self.grid.heights[agent.idx[1]][agent.idx[0]]
            self.grid.heights[agent.idx[1]][agent.idx[0]] -= 1
            
            self.voxels_moved += 1
            
            agent.num_positive += 1
            agent.num_positive_tracking += 1
            agent.num_pu += 1
        
    def deposit(self, agent, deposit_ok):
        agent.num_de_attempt += 1
        
        if deposit_ok(agent):
            agent.carrying = False
            agent.de_height = self.grid.heights[agent.idx[1]][agent.idx[0]]
            self.grid.heights[agent.idx[1]][agent.idx[0]] += 1
            
            agent.num_positive += 1
            agent.num_positive_tracking += 1
            agent.num_de += 1
        
    def move_forward(self, agent):
        if not self.__is_agent_at_index(agent.idx[0]+agent.direction_i, agent.idx[1]+agent.direction_j):
            agent.idx[0] += agent.direction_i
            agent.idx[1] += agent.direction_j
       
    def move_random(self, agent):
        movement = [-1, 0, 1]
        agent.direction_i = movement[np.abs(np.randint(0,65535) % 3)]
        agent.direction_j = movement[np.abs(np.randint(0,65535) % 3)]
        
        self.move_forward(agent)
        
    def rotate_left(self, agent):
        agent.facing = (agent.facing - 1) % 8
        
        directions = [ (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1) ]
        
        agent.direction_i = directions[agent.facing][0]
        agent.direction_j = directions[agent.facing][1]
        
    def rotate_right(self, agent):
        agent.facing = (agent.facing + 1) % 8
        
        directions = [ (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1) ]
        
        agent.direction_i = directions[agent.facing][0]
        agent.direction_j = directions[agent.facing][1]
        
    def reset(self):
        for a in self.agents:
            a.halt = False
            a.heights.clear()
            a.num_positive = 0
            a.num_positive_tracking = 0
            a.pu_height = 0
            a.de_height = 0
            
            # reinitialize agent positions
            a.idx[0] = np.random.randint(0,65535) % 16
            a.idx[1] = np.random.randint(0,65535) % 16            
            
        self.grid.reset()
        
        # reset stats
        self.voxels_moved = 0
        self.num_act_calls = 0
            
        self.reset_impl()
        
    def act(self, agent):
        self.num_act_calls += 1
        self.act_impl(agent)
        
    def act_impl(self, agent):
        raise NotImplementedError, "Err: must override act_impl() for each algorithm subclass"
        
    def reset_impl(self):
        raise NotImplementedError, "Err: must override reset_impl() for each algorithm subclass"
            
if __name__ == '__main__':
    a = AlgorithmBase(Map(16,16,8), {'num_agents':8})