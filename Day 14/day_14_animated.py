import os, imageio
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

def read_file(filename):
    with open( filename, 'r') as f:
        data = [[[int(val) for val in pair.split(',')] for pair in line.strip().split(' -> ')] for line in f]
    
    return data



def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print('\n' + 'ERROR'.center(50,'*'))
        print('Correct answer:')
        print(answer)
        print('Returned answer:')
    else:
        print('Check passed!')
    print(myanswer)



def make_gif(gif_name, pic_name, count):
    frame_len = 30 / count
    frame_len = 1.0 / 100
    with imageio.get_writer(gif_name, mode='I', duration=frame_len) as writer:
        for idx in range(0, count, 5):
            image = imageio.imread(pic_name.format(idx))
            writer.append_data(image)
        for idx in range(int(1 // frame_len)):  # pause at the end of the gif
            writer.append_data(image)




def solve(data, is_part1=True): 
    xvals, yvals = [], []
    
    '''
        Determine array size to represent the cave
    '''
    for line in data:
        for pair in line:
            xvals.append(pair[0])
            yvals.append(pair[1])
    
    xmin, xmax = min(xvals), max(xvals)
    ymin, ymax =          0, max(yvals)
    
    if not is_part1:
        # Make a larger cave for Part 2, with enough space to pyramid up the sand
        # and block the spawn
        # Also add a solid floor from side to side 2 spaces below the otherwise
        # bottom-most walls
        ymax += 2
        xmin, xmax = [max(xmin - ymax, 0), xmax + ymax]
        
        data += [[[xmin, ymax], [xmax, ymax]]]
        
    
    '''
        Populate cave with walls and spawn point
    '''
    def convert(x, y):
        # convert x,y coordinates to row, col indices
        return (np.clip(y - ymin, 0, None), np.clip(x - xmin, 0, None))

    
    cave = np.full([*convert(xmax+ 1, ymax + 1), 3], 255, dtype='uint8')
    blank = cave[0,0]  # white
    wall_color = np.array([128]*3)  # gray
    path_color = np.array([200]*3)  # lighter gray
    sand = np.array([255, 192, 0])  # orange
    spawn = convert(500, 0)
    # cave[spawn] = '+'
    
    for line in data:
        for points in zip(line[:-1], line[1:]):
            rs, cs = convert(*np.sort(points, axis = 0).T)
            cave[ rs[0]:rs[1] + 1,  cs[0]:cs[1] + 1  ] = wall_color
    
    '''
        Fill the cave with sand
    '''
    test_moves = np.array([[1, 0],   # directly down
                           [1,-1],   # down and to the left
                           [1, 1]])  # down and to the right
    
    ongrid = True  # sand is still entirely on the the grid represented in cave
    pic_idx = 0
    prefix = f"{'test' if data is test_case else 'puzz'}_Part_{'1' if is_part1 else '2'}_#"
    pic_name = os.path.join(os.path.dirname(__file__), 'gif making', prefix + '{:06d}.png')
    gif_name = os.path.join(os.path.dirname(__file__), 'gif making', prefix[:-1] + '.gif')
    pic_size = tuple(np.array(cave.shape[1::-1]) * (1000 // cave.shape[0]))
    
    def save_cave(cave, pic_idx):
        im = Image.fromarray(cave)
        im = im.resize(pic_size, Image.NEAREST)
        im.save(pic_name.format(pic_idx))
        return pic_idx + 1
    
    while ongrid:
        loc = spawn  # current location of sand block
        path = [loc]
        cave[loc] = sand  # orange for the new spot
        pic_idx = save_cave(cave, pic_idx)
        # let the block fall until it stops moving or goes out of bounds
        # each iteration = 1 move
        while True:
            canMove = False
            for new_loc in (loc + test_moves):
                # if new_loc is out of bounds of cave
                if np.any([new_loc < 0, cave.shape[:-1] <= new_loc]):
                    ongrid = False  # sand has one valid move of last resort
                elif np.all(cave[tuple(new_loc)] == blank):  # can move into air block
                    canMove = True
                    break
            
            if canMove:  # if one of the test moves was good
                cave[loc] = path_color  # lighter gray for the old spot
                loc = tuple(new_loc)
                cave[loc] = sand  # orange for the new spot
                
                pic_idx = save_cave(cave, pic_idx)
                
                path.append(tuple(loc))
                ongrid = True  # reset this since an alternative to off the board was found
                
            elif ongrid:  # the block has stopped moving without going off board
                for old_loc in path[:-1]:  # reset all the light gray squares
                    cave[old_loc] = blank
                break  # and spawn the next one
            else:  # the block went off grid
                break
        
        if np.all(loc == spawn):  # if the block couldn't move from the spawn point
            break         # ending criteria for Part 2
    
    make_gif(gif_name, pic_name, pic_idx)
    
    return np.count_nonzero(cave == sand)

prefix = "puzz_Part_1_#"
pic_name = os.path.join(os.path.dirname(__file__), 'gif making', prefix + '{:06d}.png')
gif_name = os.path.join(os.path.dirname(__file__), 'gif making', prefix[:-1] + '.gif')
make_gif(gif_name, pic_name, 65434)
    

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

# print('Part 1'.center(50,'-'))
# check( solve(test_case), 24 )
# print(solve(puzz_input))

# print('\n\n' + 'Part 2'.center(50,'-'))
# check( solve(test_case, False), 93 )
# print(solve(puzz_input, False))