import numpy as np

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

    
    cave = np.full(convert(xmax+ 1, ymax + 1), '.')
    spawn = convert(500, 0)
    cave[spawn] = '+'
    
    for line in data:
        for points in zip(line[:-1], line[1:]):
            rs, cs = convert(*np.sort(points, axis = 0).T)
            cave[ rs[0]:rs[1] + 1,  cs[0]:cs[1] + 1  ] = '#'
    
    '''
        Fill the cave with sand
    '''
    test_moves = np.array([[1, 0],   # directly down
                           [1,-1],   # down and to the left
                           [1, 1]])  # down and to the right
    
    ongrid = True  # sand is still entirely on the the grid represented in cave
    while ongrid:
        loc = spawn  # current location of sand block
        # let the block fall until it stops moving or goes out of bounds
        # each iteration = 1 move
        while True:
            canMove = False
            for new_loc in (loc + test_moves):
                # if new_loc is out of bounds of cave
                if np.any([new_loc < 0, cave.shape <= new_loc]):
                    ongrid = False  # sand has one valid move of last resort
                elif cave[tuple(new_loc)] == '.':  # can move into air block
                    canMove = True
                    break
            
            if canMove:  # if one of the test moves was good
                loc = new_loc
                ongrid = True  # reset this since an alternative to off the board was found
            elif ongrid:  # the block has stopped moving without going off board
                cave[tuple(loc)] = 'o'  # record its final spot
                break  # and spawn the next one
            else:  # the block went off grid
                break
        
        if np.all(loc == spawn):  # if the block couldn't move from the spawn point
            break         # ending criteria for Part 2
                
    return np.count_nonzero(cave == 'o')
        


test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 24 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 93 )
print(solve(puzz_input, False))