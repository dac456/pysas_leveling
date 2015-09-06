#!/usr/bin/env python

import numpy as np

from algorithm_base import *

class StatsLogger:
    
    def __init__(self, alg, num_runs):
        self.alg = alg
        self.stats = [{} for i in range(num_runs)]
        
        self.num_runs = num_runs
        
    def store_run(self, run_idx):
        self.stats[run_idx]['voxels_moved'] = self.alg.voxels_moved
        self.stats[run_idx]['avg_voxels_moved'] = float(self.alg.voxels_moved)/float(len(self.alg.agents))
        self.stats[run_idx]['act_calls'] = self.alg.num_act_calls
        self.stats[run_idx]['avg_act_calls'] = float(self.alg.num_act_calls)/float(len(self.alg.agents))
        
        self.alg.store_run(self, run_idx)
        
    def get_average_over_runs(self, stat):
       s = 0.0
       for d in self.stats:
           s += d[stat]
           
       s /= self.num_runs
       return s
       
    def get_stddev_over_runs(self, stat):
        a = []
        for d in self.stats:
            a.append(d[stat])
            
        return np.std(a)