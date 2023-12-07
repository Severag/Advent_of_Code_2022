import numpy as np

def read_file(filename):
    interp = {'.':   0,
              '>':   1,
              'v':  10,
              '<': 100,
              '^':1000,
              '#':  -1}
    
    with open( filename, 'r') as f:
        data = np.array([[interp[item] for item in line.strip()] for line in f])
    
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
    def heuristic(point_a, point_b):
        return np.sum(np.abs(np.array(point_a) - point_b))
    
    board0 = data.get_board()
    start = (0, np.where(board0[0] == 0)[0][0])
    end = (len(board0) - 1, np.where(board0[-1] == 0)[0][0])
    
    if is_part1:
        return Astar(data, start, end, 0, heuristic)
    else:
        time = data.check_path(start, 0, end)
        
        if time is None:
            time = Astar(data, start, end, 0, heuristic)
        time = Astar(data, end, start, time, heuristic)
        time = Astar(data, start, end, time, heuristic)
        return time



def Astar(graph, start, end, time0, heuristic):
    '''
    folded gscore into the state variable because the board changes, so location
    and time elapsed both define a node in the graph. ie the same spot has 
    different gscores from different times because we can stay and wait for
    # blizzards to pass
    '''
    import heapq
    
    # dist to end + time elapsed, time elapsed, location
    state = (heuristic(start, end) + time0, time0, start)
    
    open_set = {state}
    open_list = [state]
    
    closed_set = set()
        
    while open_list:
        state = heapq.heappop(open_list)
        open_set.discard(state)
        
        _, curr_time, current = state  # current time and location
        
        if state in closed_set:
            continue
        else:
            closed_set.add(state)
        
        if current == end:
            graph.add_path(start, time0, end, curr_time)
            return curr_time
        
        cand_list, board_list = graph.get_next_moves(curr_time + 1, current)
        
        for cand in cand_list:
            cand_g = curr_time + 1  # time elapsed
            cand_f = cand_g + heuristic(cand, end)  # time elapsed + dist to exit
            
            new_state = (cand_f, cand_g, cand)
            # add if new, otherwise skip
            if (new_state not in closed_set and new_state not in open_set):
                heapq.heappush(open_list, new_state)
                open_set.add(new_state)


class blizzard_tracker():
    def __init__(self, board):
        self.board_list = [board]
        self.blizz_dict = self.get_blizz_dict()
        self.paths = dict()
    
    
    def get_board(self, idx=-1):
        return self.board_list[idx]
    
    
    def add_path(self, start, t0, end, t1):
        self.paths[(start, t0, end)] = t1
    
    
    def check_path(self, start, t0, end):
        return self.paths.get((start, t0, end), None)
    
    
    def get_next_moves(self, time, loc):
        # if we don't have the state of the board for this time period
        if time >= len(self.board_list):
            # advanced it until we do
            for _ in range(len(self.board_list) - 1, time):
                self.advance_blizzards()
        
        board = self.board_list[time]
        cand_list = []
        # candidates are orthogonal adjacents spots and staying at the current spot
        for r,c in zip([0,1,0,-1,0], [0,0,1,0,-1]):
            cand = (loc[0] + r, loc[1] + c)
            
            # if the cand is within bounds and
            if 0 <= cand[0] < len(board) and 0 <= cand[1] < len(board[0]) and (
                    board[cand] == 0):  # if cand will be an open spot on the board
                cand_list.append(cand)
            
        return cand_list, self.board_list


    def advance_blizzards(self, idx=-1):
        board = self.board_list[idx]
        mod_freq = np.array(board.shape) - 2
        
        new_board = np.array(board)
        new_board[1:-1, 1:-1] = 0
            
        for r_idx, row in enumerate(board[1:-1], start=1):
            for c_idx, val in enumerate(row[1:-1], start=1):
                point = (r_idx, c_idx)
                for direc in self.blizz_dict[val]:
                    new_loc = tuple(direc + point)
                    
                    if board[new_loc] < 0:  # we've hit a wall
                        # redirect blizzard to opposite wall
                        new_loc = tuple((direc + point - 1) % mod_freq + 1)
                    
                    new_board[new_loc] += self.blizz_dict[tuple(direc)]
        
        self.board_list.append(new_board)


    def convert_to_text(self, board):
        new_board = np.full_like(board, '.', dtype=object)
        
        interp = {   0:'.',
                     1:'>',
                    10:'v',
                   100:'<',
                  1000:'^',
                    -1:'#'}
        
        for r_idx, row in enumerate(board):
            for c_idx, val in enumerate(row):
                new_board[r_idx, c_idx] = interp[val] if val in interp else str(val).count('1')
        
        return new_board


    def get_blizz_dict(self):
        blizzards = {   1:np.array([[ 0,  1]]),
                       10:np.array([[ 1,  0]]),
                      100:np.array([[ 0, -1]]),
                     1000:np.array([[-1,  0]])}
        
        # allow blizzards to convert a direction tuple back into its correpsonding key
        blizzards.update({tuple(value[0]):key for key,value in blizzards.items()})
        
        # add all other overlapping combos of blizzards converging from all directions
        for idx in range(0,16):
            key_str = f"{idx:04b}"
            key_int = int(key_str)
            
            if key_int not in blizzards:  # if it's not already
                dirs = [blizzards[10**digit][0] for digit,val in enumerate(key_str[-1::-1]) if val == '1']
                blizzards[key_int] = np.array(dirs)
        
        return blizzards
    


test_case = blizzard_tracker(read_file('test_case.txt'))
puzz_input = blizzard_tracker(read_file('puzzle_input.txt'))

print('Part 1'.center(50,'-'))
check( solve(test_case), 18 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 54 )
print(solve(puzz_input, False))