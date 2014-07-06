WIDTH=640
HEIGHT=448
COLS=10
ROWS=7
TILE_SIZE=64
board=[]

# take coordinate from GameBoard and flip the y-axis to make
# their widget position correct (since Kivy starts the y-axis at
# the bottom of the screen) and scale it up depending on tile_size
def coord2pos(x, y, size=TILE_SIZE):
    new_x = x * size
    new_y = HEIGHT - size*y - size
    #print('* x:{} -> {}\ny:{} -> {}'.format(x, new_x, y, new_y))
    new_pos = (new_x, new_y)
    return new_pos

def pos2coord(x, y, size=TILE_SIZE):
    new_x = int(x / size)
    new_y = (ROWS-1) - int(y / size)
    #print('* x:{} -> {}\ny:{} -> {}'.format(x, new_x, y, new_y))
    new_pos = (new_x, new_y)
    return new_pos 

class tiles:
    can_move = [
        '10', '11', '12',
        ]
