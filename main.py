import os
import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image



class GameBoard(GridLayout):
    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 7
        self.images = {'lava': os.path.join('assets', 'tile_lava.png')}
        self.board = []
        # create a new board and start it filled with lava
        for r in range(self.rows):
            self.board.append([])
            for c in range(self.cols):
                image = Image(source=self.images['lava'], width=64, height=64)
                image.size_hint = (None, None)
                self.board[r].append(image)
                self.add_widget(image)


class MyApp(App):
    def build(self):
        self.title = "Floor is Lava"
        Config.set('graphics', 'resizable', 0)
        Config.set('graphics', 'height', '448')
        Config.set('graphics', 'width', '640')

        return GameBoard()

if __name__ == '__main__':
    MyApp().run()
