#!/usr/bin/env python

import sys

import numpy as np
import pygame as pg

from map import *
from algorithm_base import *
from algorithm_hea_multi import *
from algorithm_standard import *
from stats_logger import *

import matplotlib.pyplot as plt

if __name__ == '__main__':
    # default sim params
    num_runs = 30
    num_terrains = 2
    
    # list of algorithm classes
    # TODO: we want to find these dynamically
    algorithms = {'hea_multi':AlgorithmHEAMulti, 'standard':AlgorithmStandard}
    
    # process cli args
    next_arg = -1
    for i,arg in enumerate(sys.argv):
        if i != 0:
            if next_arg == -1:
                if arg == "--numruns":
                    next_arg = 1
                if arg == "--numterr":
                    next_arg = 2
            else:
                if next_arg == 1:
                    num_runs = int(arg)
                    next_arg = -1
                if next_arg == 2:
                    num_terrains = int(arg)
                    next_arg = -1
    
    pg.init()
    screen = pg.display.set_mode((512,512))
    font = pg.font.SysFont("monospace", 15)
    
    N = num_terrains
    ind = np.arange(N)
    width = 0.2
    
    experiments = [(algorithms['hea_multi'](None, {'num_agents':8, 'num_chromosomes':5, 'num_steps':20, 'sense_prob':0.01, 'follow_gradient':True}),(0.0,0.0,1.0)), \
                   (algorithms['standard'](None, {'num_agents':8, 'act_prob':0.3, 'sense_prob':0.01, 'follow_gradient':True}),(0.0,1.0,0.0)), \
                   (algorithms['hea_multi'](None, {'num_agents':8, 'num_chromosomes':5, 'num_steps':20, 'sense_prob':0.01, 'follow_gradient':False}),(1.0,0.0,1.0)), \
                   (algorithms['standard'](None, {'num_agents':8, 'act_prob':0.3, 'sense_prob':0.01, 'follow_gradient':False}),(1.0,1.0,0.0))]
                   
    terrains = [Map(16, 16, 32, {'oracle_termination': True}, t) for t in range(N)
    
    u_vox = [[] for i in range(len(experiments))]
    sig_vox = [[] for i in range(len(experiments))]
    u_pos = [[] for i in range(len(experiments))]
    sig_pos = [[] for i in range(len(experiments))]
    u_act = [[] for i in range(len(experiments))]
    sig_act = [[] for i in range(len(experiments))
    labels = []
    
    for i in range(N):
        labels.append('T'+str(t)+' ('+str(grid.total_units())+')')    
    
    for e in range(len(experiments)):    
        alg = experiments[e][0]
        
        for t in range(1,N+1):
            grid = terrains[t-1]
            alg.grid = grid
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
                        
                    # draw status text
                    label = font.render('Experiment #: '+str(e)+' | Terrain #: '+str(t-1)+' | Run #: '+str(r), 1, (255,255,0))
                    screen.blit(label, (10, 10))           
                                
                    pg.display.flip()
                    
                    if not grid.is_optimal():
                        for a in alg.agents:
                            alg.act(a)
                    else:
                        run = False
                
                logger.store_run(r)
                alg.reset()
            
            # plot runs for terrain t
            u_vox[e].append(logger.get_average_over_runs('voxels_moved'))
            sig_vox[e].append(logger.get_stddev_over_runs('voxels_moved'))
            
            if alg.__class__ == AlgorithmHEAMulti:
                u_pos[e].append(logger.get_average_over_runs('avg_positive_changes'))
                sig_pos[e].append(logger.get_stddev_over_runs('avg_positive_changes'))
                
            u_act[e].append(logger.get_average_over_runs('avg_act_calls'))
            sig_act[e].append(logger.get_stddev_over_runs('avg_act_calls'))
            
    ## display charts  
    
    # voxels_moved
    plt.figure(0)
    
    fig, ax = plt.subplots()
    for i in range(len(experiments)):  
        ax.bar(ind+(width*i), tuple(u_vox[i]), width, color=experiments[i][1], yerr=tuple(sig_vox[i]))
    ax.set_title('Average voxels moved between '+str(len(alg.agents))+' agents over '+str(num_runs)+' runs')
    ax.set_ylabel('Voxels Moved') 
    ax.set_xticks(ind+width)
    ax.set_xticklabels(tuple(labels))
    
    # avg_positive_changes
    plt.figure(1)
    
    fig, ax = plt.subplots()  
    for i in range(len(experiments)):
        if experiments[i][0].__class__ == AlgorithmHEAMulti:  
            ax.bar(ind+(width*i), tuple(u_pos[i]), width, color=experiments[i][1], yerr=tuple(sig_pos[i]))
    ax.set_title('Average positive changes per chromosome between '+str(len(alg.agents))+' agents over '+str(num_runs)+' runs')
    ax.set_ylabel('Avg Positive Changes') 
    ax.set_xticks(ind+width)
    ax.set_xticklabels(tuple(labels))    
    
    # avg_act_calls
    plt.figure(2)
    
    fig, ax = plt.subplots()  
    for i in range(len(experiments)):
        ax.bar(ind+(width*i), tuple(u_act[i]), width, color=experiments[i][1], yerr=tuple(sig_act[i]))
    ax.set_title('Average act() calls between '+str(len(alg.agents))+' agents over '+str(num_runs)+' runs')
    ax.set_ylabel('Avg Calls') 
    ax.set_xticks(ind+width)
    ax.set_xticklabels(tuple(labels))      
    
    plt.show()