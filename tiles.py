import os
import sys

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.behaviors import DragBehavior

class PlayerTile(DragBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(PlayerTile, self).__init__(**kwargs)
        self.source=images[rotation]
        self.images = images
        self.rot = rotation
        # events
        self.bind(on_touch_move=self.move_callback)
    
    def move_callback(self, obj, pos):
        self.x += pos.dx
        #self.y += pos.dy


class RotTile(ButtonBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(RotTile, self).__init__(**kwargs)
        self.images = images
        self.rot = rotation
        self.bind(on_press=self.rotate_callback)

    def rotate_callback(self, obj):
        self.rot = (self.rot + 1) % 4 
        self.source = self.images[self.rot]
