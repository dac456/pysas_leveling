#!/usr/bin/env python

from algorithm_base import *

class AlgorithmHEAMulti(AlgorithmBase):
    
    Actions = enum(PICKUP=0, DEPOSIT=1, ROTATE_LEFT=2, ROTATE_RIGHT=3, MOVE=4)
    
    def __init__(self, grid, params):
        super(AlgorithmHEAMulti, self).__init__(grid, params)
        
        # initial chromosomes
        num_chromosomes = params['num_chromosomes']
        
        for a in self.agents:
            for i in range(num_chromosomes):
                a.chromosome.append((self.__generate_random_chromosome(), 0.0))
                
            a.num_evaluations = 0
        
    def __is_chromosome_valid(self, c):
        if c.count(AlgorithmHEAMulti.Actions.PICKUP) == c.count(AlgorithmHEAMulti.Actions.DEPOSIT):
            ordered = True
            for i,acti in enumerate(c):
                if acti == AlgorithmHEAMulti.Actions.PICKUP:
                    for j,actj in enumerate(c):
                        if actj == AlgorithmHEAMulti.Actions.DEPOSIT:
                            if i > j:
                                ordered = False
                                break
                                
            if ordered and c.count(AlgorithmHEAMulti.Actions.MOVE) >= 1:
                return True
            else:
                return False
        else:
            return False
            
    def __generate_random_chromosome(self):
        num_steps = self.params['num_steps']
        
        chromosome = [-1 for i in range(num_steps)]
        while not self.__is_chromosome_valid(chromosome):
            for i in range(num_steps):
                chromosome[i] = np.random.randint(0,65535) % 5
                
        return chromosome
        
    def pickup_ok(self, agent):
        return (agent.carrying == False and agent.height > agent.average() and agent.height > 0)
        
    def deposit_ok(self, agent):
        return (agent.carrying == True and agent.height < agent.average())
        
    def __read(self, agent):
        self.sense(agent)
    
    def __write(self, agent):
        step = agent.chromosome[agent.num_evaluations][0][agent.action_idx]
        
        if step == AlgorithmHEAMulti.Actions.MOVE:
            self.move_forward(agent)
        elif step == AlgorithmHEAMulti.Actions.PICKUP:
            self.pickup(agent)
        elif step == AlgorithmHEAMulti.Actions.DEPOSIT:
            self.deposit(agent)
        elif step == AlgorithmHEAMulti.Actions.ROTATE_LEFT:
            self.rotate_left(agent)
        elif step == AlgorithmHEAMulti.Actions.ROTATE_RIGHT:
            self.rotate_right(agent)
        else:
            print "invalid action"
            
        agent.action_idx = (agent.action_idx + 1) % self.params['num_steps']
        if agent.action_idx == 0:
            agent.chromosome[agent.num_evaluations] = (agent.chromosome[agent.num_evaluations][0], agent.fitness())
            
            agent.num_evaluations += 1
            agent.chromosome_idx += 1
            
            agent.num_positive = 0
            agent.num_pu = 0
            agent.num_de = 0
            agent.num_pu_attempt = 0
            agent.num_de_attempt = 0
        
    def act_impl(self, agent):
        if agent.halt == False:
            
            complete = True    
            for a in self.agents:
                if a.num_evaluations < 5:
                    complete = False            
            
            if not complete:
                if agent.read:
                    self.__read(agent)
                    agent.read = False
                else:
                    self.__write(agent)
                    agent.read = True
                    
            else:
                # generate new pool, lambda
                lambda_size = len(self.agents) * 5
                
                pool = []
                for i in range(lambda_size):
                    pool.append(self.__generate_random_chromosome())
                    
                # sort current chromosomes by fitness
                for i in range(len(self.agents)):
                    for j in range(1, self.params['num_chromosomes']):
                        k = j
                        
                        while k > 0 and self.agents[i].chromosome[k-1][1] > self.agents[i].chromosome[k][1]:
                            tmp = self.agents[i].chromosome[k]
                            self.agents[i].chromosome[k] = self.agents[i].chromosome[k-1]
                            self.agents[i].chromosome[k-1] = tmp
                            
                            k -= 1
                            
                # replace chromosomes
                pool_idx = 0
                for a in self.agents:
                    for i in range(0, self.params['num_chromosomes']-1):
                        if a.chromosome[i][1] == 0.0:
                            a.chromosome[i] = (pool[pool_idx], 0.0)
                            pool_idx += 1
                
                for a in self.agents:
                    a.num_evaluations = 0
        
    def reset_impl(self):
        for a in self.agents:
            a.action_idx = 0
        
if __name__ == '__main__':
    print help(AlgorithmHEAMulti)