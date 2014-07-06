import os
import sys

from tiles import RotTile
import const

class GameBoard:
    def __init__(self):
        self.cols = const.COLS
        self.rows = const.ROWS
        self.board = []
        self.player = [0, 0, 0] # x, y, rot
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
        for r in range(self.rows):
            line = f.readline().split(' ')
            for c in range(self.cols):
                self.board[r][c] = line[c].rstrip()
        self.pprint()
        print('entr: {}, {}\nexit: {}, {}'.format(
            self.entrance[0], self.entrance[1], self.exit[0], self.exit[1]))
