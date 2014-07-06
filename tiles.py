import os
import sys

from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

class RotTile(ButtonBehavior, Image):
    def __init__(self, images, rotation=0, **kwargs):
        super(RotTile, self).__init__(**kwargs)
        self.images = images
        self.rot = rotation
        self.bind(on_press=self.rotate_callback)

    def rotate_callback(self, obj):
        self.rot = (self.rot + 1) % 4 
        self.source = self.images[self.rot]
