import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [line.strip() for line in f]
    
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



def setup_get_indices():
    shape_dict = {'-':np.array([[0] * 4, [0,1,2,3]]).T,
                  '+':np.array([[0,-1,-1,-1,-2], [1,0,1,2,1]]).T,
                  'L':np.array([[0,0,0,-1,-2], [0,1,2,2,2]]).T,
                  '|':np.array([[0,-1,-2,-3], [0]*4]).T,
                  'B':np.array([[0,0,-1,-1], [0,1,1,0]]).T}
    
    def get_indices(rc_pair, shape):
        pairs = rc_pair + shape_dict[shape]
        if np.any(pairs < 0):
            raise IndexError('New indices are going out of bounds on the 0 end')
        return (tuple(pairs.T[0]), tuple(pairs.T[1]))
    
    return list(shape_dict.keys()), get_indices



def solve(data, is_part1=True): 
    import itertools
    rock_order, shape_func = setup_get_indices()
    
    air_dir = itertools.cycle(data[0])
    air_idx = 0
    air_nums = len(data[0])
    rock_nums = len(rock_order)

    shaft = np.full((int(20202 * 13 / 5), 7), '.')
    start_loc = (len(shaft) - 4, 2)
    loc = start_loc
    # (air index, shape index, topmost row):[row number, rock index]
    start_states = dict()  
    top_rock_spot = 0
    
    target = 2022 if is_part1 else 1_000_000_000_000
    amDebugging = False

    for rock_idx in range(0, target):
        shape = rock_order[rock_idx % rock_nums]
        
        state = (air_idx % air_nums, rock_idx % rock_nums, ''.join(shaft[top_rock_spot]))
        if state in start_states:
            # print(extrapolate(start_states[state][0], [loc[0], rock_idx], len(shaft), 2022))
            start_states[state].append([loc[0], rock_idx])
            extrap = extrapolate2(*start_states[state], len(shaft), target)
            if extrap is not None:
                return extrap
        else:
            start_states[state] = [[loc[0], rock_idx]]
        
        if air_idx % air_nums == 0 and rock_idx % rock_nums:
            amDebugging = True
        
        while True:
            # ****************
            # jets act on rock
            # ****************
            offset = 1 if next(air_dir) == '>' else -1
            air_idx += 1
            cand_loc = (loc[0], loc[1] + offset)
            
            if check_move(cand_loc, shape, shape_func, shaft):
                loc = cand_loc
            
            # ********************
            # gravity acts on rock
            # ********************
            cand_loc = (loc[0] + 1, loc[1])
            
            if check_move(cand_loc, shape, shape_func, shaft):
                loc = cand_loc
            else:
                break  # the rock landed on something
            
            if amDebugging:
                indices = shape_func(cand_loc, shape)
                shaft[indices] = '#'
                print(shaft[5231:], end='\n\n')
                shaft[indices] = '.'
        
        # record the final location
        indices = shape_func(loc, shape)  # revert to last working location
        shaft[indices] = '#'
        
        # reset loc for the starting location of the next rock
        top_rock_spot = np.where(shaft=='#')[0][0]
        loc = (top_rock_spot - 4, start_loc[1])
        # print(shaft[loc[0]:], end='\n\n')
        indices = shape_func(loc, shape) 
        # amDebugging = loc[0] < 5240 and shape == '-'

    return len(shaft) - np.where(shaft=='#')[0][0]



def check_move(cand_loc, shape, shape_func, shaft, is_gravity=False):
    try:
        indices = shape_func(cand_loc, shape)
        good_move = np.all(shaft[indices] == '.')
    except IndexError:
        good_move = False
    
    return good_move



def extrapolate(point1, point2, row_total, target):
    # points are tuples: (row number, rock number)
    # target is target number of rocks
    d_rock = point1[1] - point2[1]  # change in rock count
    d_row = point1[0] - point2[0]  # change in topmost row
    m = d_rock / d_row  # rocks/row
    b = -m * point2[0] + point2[1]  # rocks
    row_at_target = (target - b) / m
    
    # if we don't even have enough space left to fully repeat the identified 
    # pattern, then return None as the estimate
    if target - point2[1] < abs(d_rock):
        return None
    else:
        return int(row_total - row_at_target + 0.5)  # height



def extrapolate2(point1, point2, row_total, target):
    # points are tuples: (row number, rock number)
    # target is target number of rocks
    d_rock = point2[1] - point1[1]  # change in rock count
    d_row = point2[0] - point1[0]  # change in topmost row
    
    rocks_left = target - point2[1]
    # if we can repeat the pattern an integer number of times to reach the target
    if rocks_left % d_rock == 0:
        rows_left = rocks_left // d_rock * d_row
        row_at_target = rows_left + point2[0]
        return row_total - row_at_target - 4
    else:  # wait until we can meet the prior condition
        return None
    
            

# 1_000_000_000_000
test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 3068 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 1514285714288 )
print(solve(puzz_input, False))