import os
import sys
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

import glo
from gameboard import GameBoard
from player import Player
from tiles import *


class FilGame(GridLayout):
    def __init__(self, **kwargs):
        super(FilGame, self).__init__(**kwargs)
        # define tile types
        self.tiles = [] # holds all tile widgets
        self.types = {
                'arrow': {'id': 1, 'rot': True, 'mov': False},
                'start': {'id': 2, 'rot': True, 'mov': False},
                }
        self.images = self.setup_images()
        # set background image
        self.bg = Image(source=os.path.join('assets', 'bg.png'), pos=(0,0),
                width=glo.const.WIDTH, height=glo.const.HEIGHT)
        self.bg.allow_stretch = True
        self.bg.keep_ratio = False
        self.add_widget(self.bg)
        # set up game board
        self.board = GameBoard()
        self.board.load()
        # place tiles for starting level
        self.setup()

    def setup_images(self):
        images = {}
        # setup player
        images['player'] = []
        for i in range(4): # 0, 1, 2, 3
            images['player'].append(os.path.join('assets', 'player_'+str(i)+'.png')) 

        # setup tiles
        for key in self.types:
            images[key] = []
            for i in range(4): # 0, 1, 2, 3
                images[key].append(os.path.join('assets', key+'_'+str(i)+'.png')) 
        return images

    def setup(self):
        # i[0] = row number
        # i[1] = column number
        # i[2] = tile number and rotation
        #   i[2][0] = tile number
        #   i[2][1] = rotation (0=up,1=right,2=down,3=left)

        # place the tiles
        for i in self.board.boarditer():
            r, c = (int(i[0]), int(i[1]))
            tile_type = int(i[2][0])
            rotation = int(i[2][1])
            for t in self.types:
                maketile = False # flag; gets set to True when matching tile type found
                if tile_type == 0: # blank space
                    break

                if tile_type == int(self.types[t]['id']):
                    maketile = True
                    # tile can be rotated and moved pass
                    if self.types[t]['rot'] and self.types[t]['mov']: 
                        pass
                    elif self.types[t]['rot']: # tile can only be rotated
                        newtile = RotTile(self.images[t], rotation, 
                                source=self.images[t][rotation], 
                                width=glo.const.TILE_SIZE, height=glo.const.TILE_SIZE)
                    elif self.types[t]['mov']: # tile can only be moved
                        pass
                    else: # tile can't be moved or rotated
                        pass

                else: #! should never get here
                    pass

                if maketile:
                    newtile.pos = glo.coord2pos(r, c)
                    self.tiles.append(newtile)
                    self.add_widget(newtile)

        # place the player tile
        self.ptile = PlayerTile(self.images['player'], self.board.player.get_rot(),
                width=glo.const.TILE_SIZE, height=glo.const.TILE_SIZE)
        self.ptile.pos = glo.coord2pos(self.board.entrance)
        self.ptile.set_last = (self.board.entrance)
        self.add_widget(self.ptile)

    # delete all widgets before loading the next level's tiles
    def clear(self):
        for tile in self.tiles:
            self.remove_widget(tile)
        print('* Tiles cleared')
        

class FilApp(App):
    def build(self):
        self.set_sizes()
        self.title = "Floor is Lava"
        Config.set('graphics', 'resizable', 0)
        #Config.set('graphics', 'height', str(glo.const.HEIGHT))
        #Config.set('graphics', 'width', str(glo.const.WIDTH))

        return FilGame()
    
    def set_sizes(self):
        #Window.toggle_fullscreen()
        glo.const.HEIGHT = Window.height
        glo.const.WIDTH = Window.width
        sizeh = glo.const.HEIGHT / glo.const.ROWS
        sizew = glo.const.WIDTH / glo.const.COLS
        if sizeh < sizew:
            glo.const.TILE_SIZE = sizeh
        else:
            glo.const.TILE_SIZE = sizew
        glo.const.MARGIN = glo.const.HEIGHT\
                        - (glo.const.TILE_SIZE * glo.const.ROWS)

if __name__ == '__main__':
    FilApp().run()
