class const:
    WIDTH=640
    HEIGHT=448
    COLS=10
    ROWS=7
    TILE_SIZE=64
    MARGIN=0
    board=[]

# take coordinate from GameBoard and flip the y-axis to make
# their widget position correct (since Kivy starts the y-axis at
# the bottom of the screen) and scale it up depending on tile_size
def coord2pos(x, y=None):
    # if tuple/list provided instead of x,y separately
    if y == None:
        x,y = x[0], x[1]
    size = const.TILE_SIZE
    new_x = x * size
    new_y = (const.HEIGHT - size*y - size) #- const.MARGIN
    #print('* x:{} -> {}\ny:{} -> {}'.format(x, new_x, y, new_y))
    new_pos = (new_x, new_y)
    return new_pos

def pos2coord(x, y=None):
    # if tuple/list provided instead of x,y separately
    if y == None:
        x,y = x[0], x[1]
    size = const.TILE_SIZE
    margin = const.HEIGHT - (const.TILE_SIZE * const.ROWS)
    new_x = int(x / size)
    new_y = (const.ROWS-1) - int((y-margin) / size)
    #print('* x:{} -> {}\ny:{} -> {}'.format(x, new_x, y, new_y))
    new_pos = (new_x, new_y)
    return new_pos 

class tiles:
    can_move = {
        'up': [
            '10',
            '20','21','22','23',
            ],
        'right': [ 
            '11',
            '20','21','22','23',
            ],
        'down': [
            '12',
            '20','21','22','23',
            ],
        'left': [
            '13',
            '20','21','22','23',
            ],
        }

