import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [list(line.strip('\n')) for line in f]
    
    board = data[:-2]
    width = max([len(row) for row in board])
    for idx, row in enumerate(board):
        board[idx] += [' '] * (width - len(row))
    
    instr = []
    state = 'num_start'  # 'mid_num'
    for idx,char in enumerate(data[-1]):
        if char.isalpha():
            # convert number string to num
            instr[-1] = int(instr[-1]) if instr[-1].isdigit() else instr[-1]
            instr.append(char)
            state = 'num_start'
        elif state == 'num_start':
            # don't convert to int yet, because future chars might be added to it
            instr.append(char)  
            state = 'mid_num'
        else:
            instr[-1] += char
    instr[-1] = int(instr[-1]) if instr[-1].isdigit() else instr[-1]
    
    return np.array([np.array(row) for row in board]), instr
    


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
    '''
        FACING:
            0   >
            1   V
            2   <
            3   ^
    '''
    board, instr = data
    widths, heights, fix_move = get_limits(board)
    
    links = get_links(board, widths, heights)
    
    facing = np.array([[ 0,  1],
                       [ 1,  0],
                       [ 0, -1],
                       [-1,  0],])
    state = [(0, widths[0, 0]), 0]  # (row, col), facing
    
    for move in instr:
        # Move
        if isinstance(move, int):  
            
            for idx in range(move):
                if is_part1:
                    new_state = [tuple(state[0] + facing[state[1]]), state[1]]
                    
                    new_state[0] = fix_move(new_state[0], new_state[1] % 2 != 0)
                else:
                    new_state = links.get(tuple(state), None)
                    
                    if new_state is None:  # if its not an edge case
                        new_state = [tuple(state[0] + facing[state[1]]), state[1]]
                    else:  # convert outer tuple to list
                        new_state = list(new_state)
                
                try:
                    board[new_state[0]] == '#'
                except IndexError:
                    print('error')
                
                if board[new_state[0]] == '#':  # we hit a wall
                    break  # don't move and stop the movement
                
                # else
                state = new_state
                                
                board[state[0]] = ['>','V','<','^'][state[1]]
        # Rotate
        else:
            rot = 1 if move == 'R' else -1
            state[1] = (state[1] + rot) % 4
            board[state[0]] = ['>','V','<','^'][state[1]]
            
    
    return ([1000, 4] * (np.array(state[0]) + 1)).sum() + state[1]



def get_limits(board):
    widths = np.zeros((len(board), 2), dtype=int)
    heights = np.zeros((len(board.T), 2), dtype=int)
    
    for idx, row in enumerate(board):
        locs = np.where(row != ' ')
        widths[idx] = np.min(locs), np.max(locs)
    
    for idx, col in enumerate(board.T):
        locs = np.where(col != ' ')
        heights[idx] = np.min(locs), np.max(locs)
    
    # wrap moves around the box if it was about to go over
    def fix_move(pos, is_row_move):
        row, col = pos
        
        if is_row_move:
            lower, upper = heights[col]
            row2 = (row - lower) % (upper - lower + 1) + lower
            col2 = col
        else:
            lower, upper = widths[row]
            row2 = row
            col2 = (col - lower) % (upper - lower + 1) + lower
        
        return row2, col2
    
    return widths, heights, fix_move



def get_links(board, widths, heights):
    if len(board) < 20:  # the test case
        s = widths[0, 1] - widths[0, 0] + 1 # side length of cube
        corners = [(0,               widths[0,  0]),    # 0
                  (0,                widths[0,  1]),    # 1
                  (heights[0,  1],   widths[0,  1]),    # 2
                  (heights[0,  1]+1, widths[0,  1]+1),  # 3
                  (heights[0,  1]+1, widths[-1, 1]),    # 4
                  (heights[-1, 1],   widths[-1, 1]),    # 5
                  (heights[-1, 1],   widths[0,  0]),    # 6
                  (heights[0,  1]+1, widths[0,  0]),    # 7
                  (heights[0,  1],   widths[0,  0]-1),  # 8
                  (heights[0,  1],               0),    # 9
                  (heights[0,  0],               0),    #10
                  (heights[0,  0],   widths[0,  0]-1),  #11
                  (heights[0,  0]-1, widths[0,  0])]    #12
        
        # side1, side2, direction from side1, direction into side2, both increasing?
        connections = [[ 0, 11,  3,  1, -1],  
                       [ 1,  4,  0,  2, -1],
                       [ 2,  3,  0,  1, -1],
                       [ 5, 10,  1,  0, -1],
                       [ 6,  9,  1,  3, -1],
                       [ 7,  8,  2,  3,  1],
                       [12, 13,  3,  0,  1]]
    else:  # the actual problem
        s = widths[-1, 1] - widths[-1, 0] + 1 # side length of cube
        corners = [ (0,                widths[0, 0]    ),  # 0
                    (0,                widths[0, 1]    ),  # 1
                    (heights[-1, 1],   widths[0, 1]    ),  # 2
                    (heights[-1, 1],   widths[2*s, 1]+1),  # 3
                    (heights[-1, 1]+1, widths[2*s, 1]  ),  # 4
                    (heights[s,1],     widths[2*s, 1]  ),  # 5
                    (heights[s,1],     widths[0, 0]    ),  # 6
                    (heights[s,1]+1,   widths[-1, 1]   ),  # 7
                    (heights[0,1],     widths[-1, 1]   ),  # 8
                    (heights[0,1],     0               ),  # 9
                    (heights[0,0],     0               ),  # 10
                    (heights[0,0],     widths[-1, 1]   ),  # 11
                    (heights[0,0]-1,   widths[0, 0]    )]  # 12

        # side1, side2, direction from side1, direction into side2, both increasing?
        connections = [[ 0,  9, 3, 0,  1],
                       [ 1,  8, 3, 3,  1],
                       [ 2,  5, 0, 2, -1],
                       [ 3,  4, 1, 2,  1],
                       [ 6,  7, 1, 2,  1],
                       [10, 13, 2, 0, -1],
                       [11, 12, 3, 0,  1]]

    # Create lists of the points on each side, going from corner to corner
    sides = []
    for cnr1, cnr2 in zip(corners, corners[1:] + corners[:1]):
        cnr2 = np.array(cnr2)
        dist = np.abs(cnr1 - cnr2).sum() + 1
        
        if dist == 3:  # when cnr1 and cnr1 are catty-corner from each other
            continue
        
        delta = np.array((cnr2 - cnr1 + 1) // dist)
        
        for idx1 in range(0, dist, s):
            sides.append(sorted([tuple(cnr1 + delta * (idx1 + idx2)) for idx2 in range(s)]))
    
    # Create links from each point on one side to its corresponding point on the other
    # links will have keys of ((row, col), direction) for a move that would 
    #   cross over to the other side 
    #   and values of the ((row, col), direction) after the move is taken
    links = {}
    for s1, s2, dir1, dir2, sign in connections:
        temp = sides[s2] if sign > 0 else sides[s2][-1::-1]
        for sq1, sq2 in zip(sides[s1], temp):
            links[(sq1, dir1)] = (sq2, dir2)
            links[(sq2, (dir2+2) % 4)] = (sq1, (dir1+2) % 4)
    
    return links



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 6032 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 5031 )
print(solve(puzz_input, False))