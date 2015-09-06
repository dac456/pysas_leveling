#!/usr/bin/env python

import sys

import numpy as np
import pygame as pg

from map import *
from algorithm_base import *
from algorithm_hea_multi import *
from stats_logger import *

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # default sim params
    num_runs = 30
    
    # list of algorithm classes
    # TODO: we want to find these dynamically
    algorithms = {'hea_multi':AlgorithmHEAMulti}
    
    # process cli args
    next_arg = -1
    for i,arg in enumerate(sys.argv):
        if i != 0:
            if next_arg == -1:
                if arg == "--numruns":
                    next_arg = 1
            else:
                if next_arg == 1:
                    num_runs = int(arg)
                    next_art = -1
    
    screen = pg.display.set_mode((512,512))
    
    N = 2 # number of terrains to test
    ind = np.arange(N)
    width = 0.35
    
    u_vox = []
    sig_vox = []
    u_pos = []
    sig_pos = []
    labels = []
        
    for t in range(1,N+1):
        grid = Map(16, 16, 32, {'oracle_termination': True}, t)
        alg = algorithms['hea_multi'](grid, {'num_agents':8, 'num_chromosomes':5, 'num_steps':20, 'sense_prob':0.01})
        logger = StatsLogger(alg, num_runs)
        
        # initialize agent positions
        for a in alg.agents:
            a.idx[0] = np.random.randint(0,65535) % 16
            a.idx[1] = np.random.randint(0,65535) % 16        
        
        for r in range(num_runs):
            run = True
            
            while run:
                # handle pygame events
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()
                
                # draw grid cells    
                for y in range(grid.height):
                    for x in range(grid.width):
                        col = np.ceil((grid.heights[y][x]/32.0)*255)
                        pg.draw.rect(screen, (col,col,col), pg.Rect(x*32, y*32, 32, 32), 0)
                        
                # draw grid lines
                for i in range(0, 512, 32):
                    pg.draw.line(screen, (0,0,0), (0,i), (512,i), 2)
                for i in range(0, 512, 32):
                    pg.draw.line(screen, (0,0,0), (i,0), (i,512), 2)     
                    
                # draw agents
                for a in alg.agents:
                    col = (255,0,0,0)
                    if a.carrying:
                        col = (0,255,0)
                        
                    pg.draw.circle(screen, col, ((a.idx[0]*32)+16, (a.idx[1]*32)+16), 8, 0)           
                            
                pg.display.flip()
                
                if not grid.is_optimal():
                    for a in alg.agents:
                        alg.act(a)
                else:
                    run = False
            
            logger.store_run(r)
            alg.reset()
        
        # plot runs for terrain t
        u_vox.append(logger.get_average_over_runs('voxels_moved'))
        sig_vox.append(logger.get_stddev_over_runs('voxels_moved'))
        
        u_pos.append(logger.get_average_over_runs('avg_positive_changes'))
        sig_pos.append(logger.get_stddev_over_runs('avg_positive_changes'))
        
        labels.append('T'+str(t)+' ('+str(grid.total_units())+')')
            
    ## display charts  
    
    # voxels_moved
    plt.figure(0)
    
    fig, ax = plt.subplots()  
    ax.bar(ind, tuple(u_vox), width, color='r', yerr=tuple(sig_vox))
    ax.set_title('Average voxels moved between '+str(len(alg.agents))+' agents over '+str(num_runs)+' runs')
    ax.set_ylabel('Voxels Moved') 
    ax.set_xticks(ind+width)
    ax.set_xticklabels(tuple(labels))
    
    # avg_positive_changes
    plt.figure(1)
    
    fig, ax = plt.subplots()  
    ax.bar(ind, tuple(u_pos), width, color='r', yerr=tuple(sig_pos))
    ax.set_title('Average positive changes per chromosome between '+str(len(alg.agents))+' agents over '+str(num_runs)+' runs')
    ax.set_ylabel('Avg Positive Changes') 
    ax.set_xticks(ind+width)
    ax.set_xticklabels(tuple(labels))    
    
    plt.show()