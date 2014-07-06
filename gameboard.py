import os
import sys

from player import Player
from tiles import RotTile
import glo

class GameBoard:
    def __init__(self):
        self.cols = glo.COLS
        self.rows = glo.ROWS
        self.board = []
        self.player = Player(0, 0, 0) # x, y, rot
        self.entrance = [0, 0]
        self.exit = [0, 0]
        # create a new board and start it filled with empty spaces
        for r in range(self.rows):
            self.board.append([])
            for c in range(self.cols):
                self.board[r].append(0)

    # flips r and c
    def boarditer(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield (c, r, self.board[r][c])

    def clear(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c] = 0
        print("* GameBoard cleared")

    def pprint(self):
        for r in range(self.rows):
            for c in range(self.cols):
                sys.stdout.write(str(self.board[r][c]) + ' ')
            sys.stdout.write('\n')

    # house/room == world/level
    def load(self, house=0, room=0):
        # open the file for reading
        path = os.path.join('levels', str(house), str(room)+'.txt')
        f = open(path, 'r')
        print('* Level file loaded')
        # grab the level entrance location
        line = f.readline().split(',')
        self.entrance = (int(line[0]), int(line[1].rstrip()))
        # grab the level exit location
        line = f.readline().split(',')
        self.exit = (int(line[0]), int(line[1].rstrip()))
        # set the players starting rotation
        if self.entrance[0] == 0: # x=0 => facing right
            start_rot = 1 
        elif self.entrance[0] == glo.COLS-1: # facing left
            start_rot = 3 
        elif self.entrance[1] == 0: # y=0 => facing down
            start_rot = 2
        else: # facing up
            start_rot = 0 
        self.player.set_pos(self.entrance)
        self.player.set_rot(start_rot)
        print('Player is facing {}'.format(['up','down','left','right'][start_rot]))
        for r in range(self.rows):
            line = f.readline().split(' ')
            for c in range(self.cols):
                self.board[r][c] = line[c].rstrip()
        self.pprint()
        print('entr: {}, {}\nexit: {}, {}'.format(
            self.entrance[0], self.entrance[1], self.exit[0], self.exit[1]))
        glo.board = self.board
