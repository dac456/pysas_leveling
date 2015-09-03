#!/usr/bin/env python

import sys

import numpy as np
import pygame as pg

from map import *
from algorithm_base import *

if __name__ == '__main__':
    # default sim params
    num_runs = 30
    
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
    
    screen = pg.display.set_mode((512,512))
    
    grid = Map(16, 16, 8, {'oracle_termination': True})
    alg = AlgorithmBase(grid, {'num_agents':8})
    
    # initialize agent positions
    for a in alg.agents:
        a.idx[0] = np.random.randint(0,65535) % 16
        a.idx[1] = np.random.randint(0,65535) % 16
        
        
    for i in range(num_runs):
        run = True
        
        while run:
            # handle pygame events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
            
            # draw grid cells    
            for y in range(grid.height):
                for x in range(grid.width):
                    col = np.ceil((grid.heights[y][x]/8.0)*255)
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
        
        alg.reset()