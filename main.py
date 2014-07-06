import os
import sys
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

import const
from gameboard import GameBoard
from tiles import RotTile


class FilGame(GridLayout):
    def __init__(self, **kwargs):
        super(FilGame, self).__init__(**kwargs)
        # define tile types
        self.types = {
                'arrow': {'id': 1, 'rot': True, 'mov': False},
                }
        self.images = self.setup_images()
        # set background image
        self.bg = Image(source=os.path.join('assets', 'bg.png'), pos=(0,0),
                width=const.WIDTH, height=const.HEIGHT)
        self.add_widget(self.bg)
        # set up game board
        self.board = GameBoard()
        self.board.load()
        # place tiles for starting level
        self.tiles = []
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

        for i in self.board.boarditer():
            r, c = (int(i[0]), int(i[1]))
            tile_type = int(i[2][0])
            rotation = int(i[2][1])
            for t in self.types:

                if tile_type == 0: # blank space
                    break

                if tile_type == int(self.types[t]['id']):
                    # tile can be rotated and moved pass
                    if self.types[t]['rot'] and self.types[t]['mov']: 
                        pass
                    elif self.types[t]['rot']: # tile can only be rotated
                        newtile = RotTile(self.images[t], rotation, 
                                source=self.images[t][rotation], 
                                width=const.TILE_SIZE, height=const.TILE_SIZE)
                    elif self.types[t]['mov']: # tile can only be moved
                        pass
                    else: # tile can't be moved or rotated
                        pass

                else: #! should never get here
                    pass

                newtile.pos = self.fix_pos(r, c)
                self.tiles.append(newtile)
                self.add_widget(newtile)

    # delete all widgets before loading the next level's tiles
    def clear(self):
        for tile in self.tiles:
            self.remove_widget(tile)
        print('* Tiles cleared')
        
    # take pos from GameBoard and flip the y-axis to make
    # their widget position correct (since Kivy starts the y-axis at
    # the bottom of the screen)
    def fix_pos(self, x, y, size=const.TILE_SIZE):
        new_x = x * size
        new_y = self.bg.height - size*y - size
        #print('* x:{} -> {}\ny:{} -> {}'.format(x, new_x, y, new_y))
        new_pos = (new_x, new_y)
        return new_pos



class FilApp(App):
    def build(self):
        self.title = "Floor is Lava"
        Config.set('graphics', 'resizable', 0)
        Config.set('graphics', 'height', str(const.HEIGHT))
        Config.set('graphics', 'width', str(const.WIDTH))

        return FilGame()

if __name__ == '__main__':
    FilApp().run()
