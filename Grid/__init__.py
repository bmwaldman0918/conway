from datetime import date
import enum
import time
import pygame
import sys
from pygame.locals import *
import numpy as np

class pixeled:
    ## this class takes integers and turns them into pixelized versions
    ## that can then be manipulated by the rest of the game of life
    def __init__(self, x):
        if not isinstance(x, int) or x < 0:
            self.arr = np.full((5, 3), False)
            self.arr[4][1] = True
        elif x > 9:
            s = x.__str__()
            self.arr = pixeled(int(s[0])).arr
            for i in range(1, len(s)):
                self.arr = np.concatenate((self.arr, np.full((5, 1), False), pixeled(int(s[i])).arr), 1)
        elif x == 0:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((1, 1))
            change.add((2, 1))
            change.add((3, 1))
            for z in change:
                self.arr[z] = False
        elif x == 1:
            self.arr = np.full((5, 1), True)
        elif x == 2:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((1, 0))
            change.add((1, 1))
            change.add((3, 1))
            change.add((3, 2))
            for z in change:
                self.arr[z] = False
        elif x == 3:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((1, 0))
            change.add((1, 1))
            change.add((3, 0))
            change.add((3, 1))
            for z in change:
                self.arr[z] = False
        elif x == 4:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((0, 0))
            change.add((1, 1))
            change.add((3, 0))
            change.add((3, 1))
            change.add((4, 0))
            change.add((4, 1))
            for z in change:
                self.arr[z] = False
        elif x == 5:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((1, 2))
            change.add((1, 1))
            change.add((3, 0))
            change.add((3, 1))
            for z in change:
                self.arr[z] = False
        elif x == 6:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((1, 2))
            change.add((1, 1))
            change.add((3, 1))
            for z in change:
                self.arr[z] = False
        elif x == 7:
            self.arr = np.full((5, 3), False)
            change = set()
            change.add((0, 0))
            change.add((0, 1))
            change.add((0, 2))
            change.add((1, 2))
            change.add((2, 1))
            change.add((3, 1))
            change.add((4, 1))
            for z in change:
                self.arr[z] = True
        elif x == 8:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((1, 1))
            change.add((3, 1))
            for z in change:
                self.arr[z] = False
        else:
            change = set()
            self.arr = np.full((5, 3), True)
            change.add((1, 1))
            change.add((3, 0))
            change.add((3, 1))
            change.add((4, 0))
            change.add((4, 1))
            for z in change:
                self.arr[z] = False

class grid:  
    ## this class represents the actual game
    def __init__(self, d:date=date.today(), xbuffer:int=0, ybuffer:int=0):
        ## accepts a date variable (or by default uses today date)
        ## e.g. date(year=2002, month=9, day=18)
        ##
        ## the xbuffer and ybuffer variables control the amount of usable blank space
        ## the game can expand into in the x and y directions, respectively
        self.today = d
        
        ## creates a matrix initialized with pixeled representations of the day, month, and year
        self.matrix = np.concatenate((pixeled(self.today.day).arr, 
                                      pixeled(-1).arr,
                                      pixeled(self.today.month).arr,
                                      pixeled(-1).arr,
                                      pixeled(self.today.year).arr), 1)
        if xbuffer > 0:
            c = self.matrix.shape[0]
            self.matrix = np.concatenate((np.full((c, xbuffer), False), 
                                          self.matrix, 
                                          np.full((c, xbuffer), False)), 
                                          1)
        if ybuffer > 0:
            r = self.matrix.shape[1]
            self.matrix = np.concatenate((np.full((ybuffer, r), False), 
                                          self.matrix, 
                                          np.full((ybuffer, r), False)), 
                                          0)
            
        self.col_count = self.matrix.shape[0]
        self.row_count = self.matrix.shape[1]
            
            
    def next(self):
        ## creates a new matrix
        updated = np.ndarray.copy(self.matrix)
        
        ## iterators through each column in the matrix
        for col in range(self.col_count):
            ## iterates through each row in the matrix
            for row in range(self.row_count):
                ## self.matrix[col][row] is the "current cell" in the matrix
                ## now we count its neighbors
                
                ## counter for the number of alive neighbors
                neighbors = 0
                ## searches the cells around the current cell
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        try:
                            ## if the neighbor is alive, add it to the alive neighbors counts
                            if ((not ((i == 0) and (j == 0)))
                                and self.matrix[col + i][row + j]):
                                neighbors = neighbors + 1
                        except IndexError:
                            pass
                
                ## if the current cell is alive
                if (self.matrix[col][row]):
                    ## and it doesn't have 2 or 3 alive neighbors
                    if(not (neighbors == 2 or neighbors == 3)):
                        ## kill it in the new matrix
                        updated[col][row] = False
                        
                ## if the current cell is dead
                else:
                    ## and it has three alive neighbors
                    if(neighbors == 3):
                        ## make it alive in the new matrix
                        updated[col][row] = True
                        
        ## set the current matrix to be the update matrix
        self.matrix = updated
        
    def __str__(self):
        ## returns a visual representation of a current grid
        ## alive cells are represented by an 'X' and dead cells are represented by an 'O'
        s = ""
        for col in range(self.col_count):
            for row in range(self.row_count):
                if self.matrix[col][row]:
                    s = s + "X "
                else:
                    s = s + "O "
            s = s.removesuffix(" ")
            s = s + "\n"
        s.removesuffix("\n")
        return s
    
    def run(self, scale=10, buffer=0):
        ## accepts a scale variable that scales up or down the size of the display
        ## accepts a buffer variable that creates a border of nonusable dead space around
        ## the display
        pygame.init()
        size = width, height = ((self.row_count + buffer) * scale), ((self.col_count + buffer) * scale)
        display = pygame.display.set_mode(size)
        black = [0, 0, 0]
        green = [0, 255, 0]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                    
            display.fill(black)
            end = True
            for col in range(self.col_count):
                for row in range(self.row_count):
                    if self.matrix[col][row]:
                        end = False
                        pygame.draw.rect(display, 
                                         green, 
                                         pygame.Rect(((row + (buffer / 2)) * scale, 
                                                      (col + (buffer / 2)) * scale), 
                                                     (scale, scale)))
            
            pygame.display.flip()
            if end:
                time.sleep(3)
                sys.exit()
            self.next()
            time.sleep(1)

## date objects should be entered in year, month, day format
## in the test below, 2002 is the year, 9 is the month, and 18 is the day
grid(date(2002, 9, 18), xbuffer=3, ybuffer=8).run(scale=20, buffer=3)