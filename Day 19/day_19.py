import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [[int(val) for val in line.strip().split(' ') if val.isnumeric()] for line in f]
    
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
    limit = 24  # minutes
    
    if not is_part1:
        data = data[:3]
        limit = 32
    scores = []
    
    for idx, blueprint in enumerate(data):
        actions = np.zeros((4,9), dtype=int)  # 1 row for each robot, columns defined in get_quality()
        res_idx = 5  # index where resources start
        
        for row, i in enumerate([0, 1, 2, 4]):
            actions[row, row+1] = 1  # add the robot in question
            actions[row, res_idx] = -blueprint[i]  # set ore cost for this robot
            
            if row == 2:  # set clay cost for obsidian robot
                actions[row, res_idx+1] = -blueprint[i+1]
            elif row == 3:  # set obsidian cost for geode robot
                actions[row, res_idx+2] = -blueprint[i+1]
        
        scores.append(get_quality(actions, limit))
    
    print('')
    if is_part1:
        return sum([idx*val for idx, val in enumerate(scores, start=1)])
    else:
        return np.prod(scores)



def get_quality(actions, total_time):
    import heapq
    #       time ore clay obsidian geode
    state0 = [0,  1,   0,    0,      0,  # robots
                  0,   0,    0,      0]  # resources
    state0 = np.array(state0)
    rob_idx = 1
    res_idx = 5
    cap = np.max(-actions[:, res_idx:], axis=0)
    
    def rank(state):
        gain = state[-1]
        return [-gain, tuple(state)]
    
    open_list = [rank(state0)]
    closed_list = set()
    best_q = 0
    
    while open_list:
        state = np.array(list(heapq.heappop(open_list)[-1]))
        state_tup = tuple(state)
        
        # if len(closed_list) % 100000 == 0:
        #     print(len(closed_list), best_q, len(open_list))
        
        if state_tup not in closed_list:
            closed_list.add(state_tup)
            
            ''' is this state worth propagating? '''
            time = state[0]
            d_time = total_time - time
            # assuming we could build a geode bot every turn (best case scenario),
            # if we can't outdo the current best, don't bother trying
            if d_time * ((d_time+1)/2 + state[rob_idx+3]) + state[-1] < best_q:
                continue
                        
            didnt_build = True
            bots = state[rob_idx:res_idx]
            cur_res = state[res_idx:] 
            
            '''' choose what to build next '''
            for idx, act in enumerate(actions):  # for each type of bot
                req_res = -act[res_idx:] 
                
                # if we can produce this robot
                if np.all((bots > 0) >= (req_res > 0)):
                    # calculate number of turns to get required resources
                    d_time = int(np.ceil(np.nanmax((req_res - cur_res) / bots))) + 1
                    d_time = max(d_time, 1)  # d_time has to be at least 1
                    
                    # once we meet the resource needs of building any bot in 1 turn
                    # don't bother building anymore of that resource, except geode bots
                    still_needed = idx == 3 or (state[rob_idx + idx] < cap[idx])
                    
                    # if we can build it within the allotted time and 
                    # do we need any more of them
                    if time + d_time < total_time and still_needed:
                        didnt_build = False
                        
                        delta = np.zeros_like(state0)
                        delta[0] = d_time  # add minutes
                        delta[res_idx:] = bots * d_time  # work done by robots
                        
                        heapq.heappush(open_list, rank(state + delta + act))
                        
            '''' ran out of time to build anything '''
            if didnt_build:  
                d_time = total_time - time
                
                delta = np.zeros_like(state0)
                delta[0] = d_time  # add minutes
                delta[res_idx:] = bots * d_time  # work done by robots
                
                new_state = tuple(state + delta)
                
                closed_list.add(new_state)
                best_q = max(best_q, new_state[-1])
                
    print(best_q, end=', ')
    return best_q



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 33 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 3472 )
print(solve(puzz_input, False))