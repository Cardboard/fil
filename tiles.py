import os
import sys
from functools import partial

from kivy.clock import Clock
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
                if self.check_move(x, y, 'right'):
                    self.x += mouse.dx
                else:
                    self.snap('x')
            elif mouse.dx < 0 and self.x > 0:
                if self.check_move(x, y, 'left'):
                    self.x += mouse.dx

            # VERTICAL MOVEMENT
            if mouse.dy > 0 and y < glo.const.ROWS-1:
                if self.check_move(x, y, 'up'):
                    self.y += mouse.dy
                else:
                    self.snap('y')
            elif mouse.dy < 0 and self.y > 0:
                if self.check_move(x, y, 'down'):
                    self.y += mouse.dy

    # check to see if the move is valid
    def check_move(self, x, y, direc):
        # can't move because edge of map
        if x < 0 or x >= glo.const.COLS or y < 0 or y >= glo.const.ROWS:
            return False
        # directional movement
        if direc == 'right':
            t0 = glo.const.board[y][x]
            t1 = glo.const.board[y][x+1]
            t2 = glo.const.board[y][x+2]
            # check to make sure we can move right from the tile we're on
            # we are checking left tiles because it is set up so that 
            # tiles in ['left'] are the tiles we can't move left ONTO,
            # meaning we can't move right OFF OF them

            # we can also move right if we are already on lava and the tile
            # to the right is able to be moved onto
            if t0 not in glo.tiles.can_move['left'] and not t0 == '00':
                return False
            # check the tile to the right to see if we can move left onto it
            if t1 in glo.tiles.can_move['right']:
                if t0 != '00':
                    self.save_last(x, None)
                return True
            # check to see if we are moving OVER lava into a space we can move onto
            if t1 == '00' and t2 in glo.tiles.can_move['right']:
                return True
        elif direc == 'left':
            # check to see if the move has just started,
            # since the origin of the tile is on the left, so
            # immediately after moving the current tile changes,
            # as opposed to moving right, where the tile is constant
            # until the tile has moved all the way
            if self.x % glo.const.TILE_SIZE == 0:
                t0 = glo.const.board[y][x]
                t1 = glo.const.board[y][x-1]
                t2 = glo.const.board[y][x-2]
            else:
                t0 = glo.const.board[y][x+1]
                t1 = glo.const.board[y][x]
                t2 = glo.const.board[y][x-1]
            # see comments above for better explanation of the rest

            # make sure we can move left off the current tile,
            # or are on lava (in the middle of a movement over lava)
            if t0 not in glo.tiles.can_move['right'] and not t0 == '00':
                return False
            # make sure we can move left onto the destination tile
            if t1 in glo.tiles.can_move['left']:
                if t0 != '00':
                    self.save_last(x, None)
                return True
            # if we are on lava and the tile after is valid, we can move
            if t1 == '00' and t2 in glo.tiles.can_move['left']:
                return True

        elif direc == 'down':
            if self.y % glo.const.TILE_SIZE == glo.const.MARGIN:
                t0 = glo.const.board[y][x]
                t1 = glo.const.board[y+1][x]
                t2 = glo.const.board[y+2][x]
            else:
                t0 = glo.const.board[y-1][x]
                t1 = glo.const.board[y][x]
                t2 = glo.const.board[y+1][x]
            # move off current tile is valid (or are on lava)
            if t0 not in glo.tiles.can_move['up'] and not t0 == '00':
                return False
            # move onto adjacent tile is valid
            if t1 in glo.tiles.can_move['down']:
                if t0 != '00':
                    self.save_last(None, y)
                return True
            # on lava and move onto adjacent tile is valid
            if t1 == '00' and t2 in glo.tiles.can_move['down']:
                return True

        elif direc == 'up':
            t0 = glo.const.board[y][x]
            t1 = glo.const.board[y-1][x]
            t2 = glo.const.board[y-2][x]
            # move off current tile is valid (or on lava)
            if t0 not in glo.tiles.can_move['down'] and not t0 == '00':
                return False
            # move onto adjacent tile is valid
            if t1 in glo.tiles.can_move['up']:
                if t0 != '00':
                    self.save_last(None, y)
                return True
            # on lava and move onto adjacent tile is valid
            if t1 == '00' and t2 in glo.tiles.can_move['up']:
                return True
    
    # saves the last position of the player 
    # on a valid tile (not in lava) 
    # ((so we can move him back if he tries to
    # end his movement in lava like a moron))
    def save_last(self, x=None, y=None):
        if x != None and self.last[0] != x:
            self.last[0] = x
        if y != None and self.last[1] != y:
            self.last[1] = y
        glo.const.pcoord = self.last

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
            x, y = glo.pos2coord(self.x, self.y)
            self.save_last(x, y)


class MovRotTile(ButtonBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(MovRotTile, self).__init__(**kwargs)
        self.allow_stretch = True
        self.images = images
        self.rot = rotation
        self.bind(on_touch_down=self.action_callback)
        self.waiting = True

    # filters out single and double clicks then calls the correct callback
    def action_callback(self, obj, mouse):
        is_adj, direc = self.is_adj_player()
        if is_adj: # make sure player is adjacent to the tile
            if self.collide_point(mouse.x, mouse.y):
                if mouse.is_double_tap and self.waiting:
                    self.rotate_callback(obj, mouse)
                    self.waiting = False
                else:
                    self.waiting = True
                    Clock.schedule_once(partial(self.check_double_tap, obj, mouse, direc), 0.2)

    # check to see if a double tap has occured while waiting a bit
    # if not, register the first tap as a single tap
    def check_double_tap(self, obj, mouse, direc, dt):
        if self.waiting:
            self.move_callback(obj, mouse, direc)
            self.waiting = False
        
    def rotate_callback(self, obj, mouse):
        # update the tile's image
        self.rot = (self.rot + 1) % 4 
        self.source = self.images[self.rot]
        # update the board
        x,y = glo.pos2coord(self.x, self.y)
        glo.const.board[y][x] = glo.const.board[y][x][0] + str(self.rot)
        self.double = False

    # move a tile that is adjacent to the player
    def move_callback(self, obj, mouse, direc):
        x, y = glo.pos2coord(self.x, self.y)
        tile = glo.const.board[y][x]
        if direc == 'up': # push tile upwards
            glo.const.board[y][x] = '00'
            y -= 1
            glo.const.board[y][x] = tile 
        elif direc == 'down':
            glo.const.board[y][x] = '00'
            y += 1
            glo.const.board[y][x] = tile 
        elif direc == 'right':
            glo.const.board[y][x] = '00'
            x += 1
            glo.const.board[y][x] = tile 
        elif direc == 'left':
            glo.const.board[y][x] = '00'
            x -= 1
            glo.const.board[y][x] = tile 
        self.x, self.y = glo.coord2pos(x, y)

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

    def is_adj_player(self):
        is_adj = False
        direc = None
        x, y = glo.pos2coord(self.x, self.y)
        px, py = glo.const.pcoord # get player's current coordinate
        # tile is to the left or right of the player
        if abs(x - px) == 1 and abs(y - py) == 0:
            is_adj = True
            if x < px:
                direc = 'left'
            else:
                direc = 'right'
        # tile is to the top or bottom of the player
        elif abs(y - py) == 1 and abs(x - px) == 0:
            is_adj = True
            if y < py:
                direc = 'up'
            else:
                direc = 'down'

        return [is_adj, direc]


class MovTile(ButtonBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(MovTile, self).__init__(**kwargs)
        self.allow_stretch = True
        self.images = images
        self.rot = rotation
        self.bind(on_touch_down=self.action_callback)
        self.waiting = True

    # filters out single and double clicks then calls the correct callback
    def action_callback(self, obj, mouse):
        is_adj, direc = self.is_adj_player()
        if is_adj: # make sure player is adjacent to the tile
            if self.collide_point(mouse.x, mouse.y):
                # double click does nothing for MovTiles
                if mouse.is_double_tap and self.waiting:
                    self.waiting = False
                else:
                    self.waiting = True
                    Clock.schedule_once(partial(self.check_double_tap, obj, mouse, direc), 0.2)

    # check to see if a double tap has occured while waiting a bit
    # if not, register the first tap as a single tap
    def check_double_tap(self, obj, mouse, direc, dt):
        if self.waiting:
            self.move_callback(obj, mouse, direc)
            self.waiting = False
        
    # move a tile that is adjacent to the player
    def move_callback(self, obj, mouse, direc):
        x, y = glo.pos2coord(self.x, self.y)
        tile = glo.const.board[y][x]
        if direc == 'up': # push tile upwards
            glo.const.board[y][x] = '00'
            y -= 1
            glo.const.board[y][x] = tile 
        elif direc == 'down':
            glo.const.board[y][x] = '00'
            y += 1
            glo.const.board[y][x] = tile 
        elif direc == 'right':
            glo.const.board[y][x] = '00'
            x += 1
            glo.const.board[y][x] = tile 
        elif direc == 'left':
            glo.const.board[y][x] = '00'
            x -= 1
            glo.const.board[y][x] = tile 
        self.x, self.y = glo.coord2pos(x, y)

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

    def is_adj_player(self):
        is_adj = False
        direc = None
        x, y = glo.pos2coord(self.x, self.y)
        px, py = glo.const.pcoord # get player's current coordinate
        # tile is to the left or right of the player
        if abs(x - px) == 1 and abs(y - py) == 0:
            is_adj = True
            if x < px:
                direc = 'left'
            else:
                direc = 'right'
        # tile is to the top or bottom of the player
        elif abs(y - py) == 1 and abs(x - px) == 0:
            is_adj = True
            if y < py:
                direc = 'up'
            else:
                direc = 'down'

        return [is_adj, direc]

class RotTile(ButtonBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(RotTile, self).__init__(**kwargs)
        self.allow_stretch = True
        self.images = images
        self.rot = rotation
        self.bind(on_touch_down=self.rotate_callback)
        self.waiting = True
        
    def rotate_callback(self, obj, mouse):
        # only rotate the tile if the player is next to it
        if self.is_adj_player()[0]: # is_adj_player returns [bool, direction]
            # the mouse collides with the tile and is a double click
            if self.collide_point(mouse.x, mouse.y) and mouse.is_double_tap:
                # update the tile's image
                self.rot = (self.rot + 1) % 4 
                self.source = self.images[self.rot]
                # update the board
                x,y = glo.pos2coord(self.x, self.y)
                glo.const.board[y][x] = glo.const.board[y][x][0] + str(self.rot)
                self.double = False

    def is_lava(self, x, y=None):
        if y == None:
            x,y = x[0], x[1]
        return glo.const.board[y][x] == '00'

    # snap the player tile to the grid upon release
    def snap(self, direc):
        x, y = glo.pos2coord(
                self.x + glo.const.tile_size/2,
                self.y + glo.const.tile_size/2)
        newx, newy = glo.coord2pos(x,y)
        if 'x' in direc:
            self.x = newx
        if 'y' in direc:
            self.y = newy

    def is_adj_player(self):
        is_adj = False
        direc = None
        x, y = glo.pos2coord(self.x, self.y)
        px, py = glo.const.pcoord # get player's current coordinate
        # tile is to the left or right of the player
        if abs(x - px) == 1 and abs(y - py) == 0:
            is_adj = True
            if x < px:
                direc = 'left'
            else:
                direc = 'right'
        # tile is to the top or bottom of the player
        elif abs(y - py) == 1 and abs(x - px) == 0:
            is_adj = True
            if y < py:
                direc = 'up'
            else:
                direc = 'down'
        
        return [is_adj, direc]

class Tile(Image):
    def __init__(self, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.allow_stretch = True
