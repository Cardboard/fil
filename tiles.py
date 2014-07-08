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
        self.last = [0, 0]
        # drag props
        self.drag_rectangle = self.x, self.y, glo.const.TILE_SIZE, glo.const.TILE_SIZE
        # events
        self.bind(on_touch_move=self.move_callback)
        self.bind(on_touch_up=self.release_callback)

    def set_last(self, pos):
        self.last = pos

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
                if self.check_tile(x+1, y, 'right'):
                    self.save_last(x-1, y)
                    self.x += mouse.dx
                elif self.check_tile(x+2, y, 'right') and self.is_lava(x+1, y):
                    self.x += mouse.dx
                else:
                    self.snap('x')
            elif mouse.dx < 0 and self.x > 0:
                if self.x % glo.const.TILE_SIZE == 0:
                    if self.check_tile(x-1, y, 'left'):
                        self.x += mouse.dx
                    elif self.check_tile(x-2, y, 'left') and self.is_lava(x-1, y):
                        self.x += mouse.dx
                    else:
                        self.snap('x')
                else:
                    if self.check_tile(x, y, 'left'):
                        self.save_last(x+2, y)
                        self.x += mouse.dx
                    elif self.check_tile(x-1, y, 'left') and self.is_lava(x, y):
                        self.x += mouse.dx
                    else:
                        self.snap('x')

            # VERTICAL MOVEMENT
            if mouse.dy > 0 and y < glo.const.ROWS-1:
                if self.check_tile(x, y-1, 'up'):
                    self.save_last(x, y+1)
                    self.y += mouse.dy
                elif self.check_tile(x, y-2, 'up') and self.is_lava(x, y-1):
                    self.y += mouse.dy
                else:
                    self.snap('y')
            elif mouse.dy < 0 and self.y > 0:
                if self.y % glo.const.TILE_SIZE == glo.const.MARGIN:
                    if self.check_tile(x, y+1, 'down'):
                        self.y += mouse.dy
                    elif self.check_tile(x, y+2, 'down') and self.is_lava(x, y+1):
                        self.y += mouse.dy
                    else:
                        self.snap('y')
                else:
                    if self.check_tile(x, y, 'down'):
                        self.save_last(x, y-2)
                        self.y += mouse.dy
                    elif self.check_tile(x, y+1, 'down') and self.is_lava(x, y):
                        self.y += mouse.dy
                    else:
                        self.snap('y')

    # check to see if the tile is able to be moved to
    def check_tile(self, x, y, direc):
        if x < 0 or x >= glo.const.COLS or y < 0 or y >= glo.const.ROWS:
            return False
        return glo.const.board[y][x] in glo.tiles.can_move[direc]
    
    # saves the last position of the player 
    # on a valid tile (not in lava) 
    # ((so we can move him back if he tries to
    # end his movement in lava like a moron))
    def save_last(self, x, y):
        self.last = [x, y]

    def is_lava(self, x, y=None):
        if y == None:
            x,y = x[0], x[1]
        return glo.const.board[y][x] == '00'

    # snap the player tile to the grid upon release
    def snap(self, direc):
        x, y = glo.pos2coord(
                self.x + glo.const.TILE_SIZE/2,
                self.y + glo.const.TILE_SIZE/2)
        newx, newy = glo.coord2pos(x,y)
        if 'x' in direc:
            self.x = newx
        if 'y' in direc:
            self.y = newy

    def release_callback(self, obj, mouse):
        # if the player ends on a lava space, move them
        # back to the last valid tile they were on
        self.snap('xy')
        if self.is_lava(glo.pos2coord(self.x, self.y)):
            self.x, self.y = glo.coord2pos(self.last)
        else:
            self.last = glo.pos2coord(self.x, self.y)


class RotTile(ButtonBehavior, Image):
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

    def is_lava(self, x, y=None):
        if y == None:
            x,y = x[0], x[1]
        return glo.const.board[y][x] == '00'

    # snap the player tile to the grid upon release
    def snap(self, direc):
        x, y = glo.pos2coord(
                self.x + glo.const.TILE_SIZE/2,
                self.y + glo.const.TILE_SIZE/2)
        newx, newy = glo.coord2pos(x,y)
        if 'x' in direc:
            self.x = newx
        if 'y' in direc:
            self.y = newy
