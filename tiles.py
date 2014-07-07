import os
import sys

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import DragBehavior

import glo

class PlayerTile(DragBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(PlayerTile, self).__init__(**kwargs)
        self.allow_stretch = True
        self.source=images[rotation]
        self.images = images
        self.rot = rotation
        # drag props
        self.drag_rectangle = self.x, self.y, glo.const.TILE_SIZE, glo.const.TILE_SIZE
        # events
        self.bind(on_touch_move=self.move_callback)
        self.bind(on_touch_up=self.release_callback)

    # drag the player tile if the mouse collides with it while pressed
    def move_callback(self, obj, mouse):
        # mouse collides with player tile
        if self.collide_point(mouse.x, mouse.y):
            # check board to see if the move is valid
            # we need to check the left side of the tile for moves to the right
            # and the right side of the tile for moves to the left
            # so that the
            x,y = glo.pos2coord(self.x, self.y) # left side of tile

            # checks the appropriate board space in glo.const.board
            # depending on whether dx/dy are positive or negative
            # and returns True if the player can move where the user
            # wants it to

            # HORIZONTAL MOVEMENT
            if mouse.dx > 0 and x < glo.const.COLS-1:
                if glo.const.board[y][x+1] in glo.tiles.can_move['right']:
                    self.x += mouse.dx
            elif mouse.dx < 0 and self.x > 0:
                if self.x % glo.const.TILE_SIZE == 0:
                    if glo.const.board[y][x-1] in glo.tiles.can_move['left']:
                        self.x += mouse.dx
                else:
                    if glo.const.board[y][x] in glo.tiles.can_move['left']:
                        self.x += mouse.dx

            # VERTICAL MOVEMENT
            if mouse.dy > 0 and y < glo.const.ROWS-1:
                if glo.const.board[y-1][x] in glo.tiles.can_move['up']:
                    self.y += mouse.dy
            elif mouse.dy < 0 and self.y > 0:
                if self.y % glo.const.TILE_SIZE == glo.const.MARGIN:
                    if glo.const.board[y+1][x] in glo.tiles.can_move['down']:
                        self.y += mouse.dy
                else:
                    if glo.const.board[y][x] in glo.tiles.can_move['down']:
                        self.y += mouse.dy

    # snap the player tile to the grid upon release
    def release_callback(self, obj, mouse):
        # mouse collides with player tile
        x, y = glo.pos2coord(
                self.x + glo.const.TILE_SIZE/2,
                self.y + glo.const.TILE_SIZE/2)
        self.x, self.y = glo.coord2pos(x, y)


class RotTile(DragBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(RotTile, self).__init__(**kwargs)
        self.allow_stretch = True
        self.images = images
        self.rot = rotation
        self.bind(on_touch_down=self.rotate_callback)

    def rotate_callback(self, obj, mouse):
        if self.collide_point(mouse.x, mouse.y) and mouse.is_double_tap:
            # update the tile's image
            self.rot = (self.rot + 1) % 4 
            self.source = self.images[self.rot]
            # update the board
            x,y = glo.pos2coord(self.x, self.y)
            glo.const.board[y][x] = glo.const.board[y][x][0] + str(self.rot)
