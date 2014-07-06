import os
import sys

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import DragBehavior

import glo

class PlayerTile(DragBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(PlayerTile, self).__init__(**kwargs)
        self.source=images[rotation]
        self.images = images
        self.rot = rotation
        # drag props
        self.drag_rectangle = self.x, self.y, glo.TILE_SIZE, glo.TILE_SIZE
        # events
        self.bind(on_touch_move=self.move_callback)
        self.bind(on_touch_up=self.release_callback)
    
    # drag the player tile if the mouse collides with it while pressed
    def move_callback(self, obj, mouse):
        # mouse collides with player tile
        if self.collide_point(mouse.x, mouse.y):
            # check board to see if the move is valid
            x,y = glo.pos2coord(self.x, self.y)

            # mouse moved right, check right space
            if mouse.dx > 0 and x < glo.COLS-1:
                if glo.board[y][x+1] in glo.tiles.can_move:
                    self.x += mouse.dx
            elif mouse.dx < 0 and self.x > 0:
                if glo.board[y][x-1] in glo.tiles.can_move:
                    self.x += mouse.dx

            #self.y += mouse.dy

    # snap the player tile to the grid upon release
    def release_callback(self, obj, mouse):
        # mouse collides with player tile
        x, y = glo.pos2coord(
                self.x + glo.TILE_SIZE/2,
                self.y + glo.TILE_SIZE/2)
        self.x, self.y = glo.coord2pos(x, y)




class RotTile(ButtonBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(RotTile, self).__init__(**kwargs)
        self.images = images
        self.rot = rotation
        self.bind(on_press=self.rotate_callback)

    def rotate_callback(self, obj):
        # update the tile's image
        self.rot = (self.rot + 1) % 4 
        self.source = self.images[self.rot]
        # update the board
        x,y = glo.pos2coord(self.x, self.y)
        glo.board[y][x] = glo.board[y][x][0] + str(self.rot)
