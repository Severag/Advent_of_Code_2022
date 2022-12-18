import numpy as np

def read_file(filename):
    def parse_line(line):
        import re
        items = re.split('Valve | has flow rate=|; tunnels lead to valves |; tunnel leads to valve |, ', line)[1:]
        items[1] = int(items[1])
        return items
    
    
    with open( filename, 'r') as f:
        data = [parse_line(line.strip()) for line in f]
    
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



def Astar(info, start, end, dist, heuristic):
    # connections, flow_rates, valve2idx
    connections, flow_rates, index_valve = info
    import heapq, itertools
    
    gscores = {start.tobytes():0}
    fscores = {start.tobytes():heuristic(start, end) + 0}
    tiebreaker = itertools.count(0, -1)
    
    open_set = {start.tobytes()}
    open_list = [(fscores[start.tobytes()], 0, next(tiebreaker), start.tobytes())]  # (cost, (-)cumlative pressure released, state)
    
    closed_set = set()
    
    end_time = 30 * dist()
    
    max_r = np.sum(flow_rates)
    # best = [total flow, state (in byte-form)]
    best = [0, start]
    
    while open_list:
        old_f, old_flow, _, current_bytes = heapq.heappop(open_list)
        # current state
        current = np.frombuffer(bytearray(current_bytes), dtype=start.dtype).reshape(start.shape)
        # current node
        cur_node_num = current[0, -1]
        open_set.discard(current_bytes)
        
        # if we've already visited
        if current_bytes in closed_set:
            continue
        else:
            closed_set.add(current_bytes)
        
        # if time's up
        if gscores[current_bytes] >= end_time:
            # if this path achieved more total flow
            if np.abs(old_flow) > best[0]:
                # make it the current best
                best = [np.abs(old_flow), current_bytes]            
            # doesn't need to be iterated anymore
            continue
        
        # if we have a 'best' to benchmark
        if best[0] > 0:
            time_left = (end_time - gscores[current_bytes] + 1) // dist()
            # if this path can't exceed the current best, even with max flow rate
            # for the rest of the time, don't bother propagating it anymore
            if best[0] > np.abs(old_flow) + time_left * max_r:
                continue
            
        
        
        # if current has opened all the valves
        if np.count_nonzero(flow_rates) - np.count_nonzero(current[:, 0]) == 0:
            # don't produce more children, just propagate forward
            current[:, 1] += current[:, 0]
            candidates = [current]
        else:
            candidates = get_new_states(current, connections[cur_node_num], index_valve, flow_rates)
        
        
        for cand in candidates:
            cand_bytes = cand.tobytes()
            cand_g = gscores[current_bytes] + dist(current, cand, None)
            cand_f = cand_g + heuristic(cand, end)
            
            # add if new
            # update previous entry if this one is better
            # otherwise skip
            if (cand_bytes not in closed_set and cand_bytes not in open_set) or (gscores.get(cand_bytes, np.inf) > cand_g):
                heapq.heappush(open_list, (cand_f, -total_flow(cand, flow_rates), next(tiebreaker), cand_bytes))
                open_set.add(cand_bytes)
                
                gscores[cand_bytes] = cand_g
                fscores[cand_bytes] = cand_f
        
        # if len(happy_set & open_set) < 1:
        #     print('warning?')
        if len(closed_set) % 10_000 == 0:
            print(best[0], len(open_list))
                    
        
    return best[0]



def total_flow(state, flow_rates):
    return np.sum(state[:, 1] * flow_rates)



def get_new_states(state, neighbors, index_valve, flow_rates):
    cur_idx = state[0, -1]
    # if the current valve hasn't been turned on yet, add the option of spending
    # the minute turning it on, but only if it has a positive flow rate
    neighbors = neighbors + ([] if state[cur_idx, 0] > 0 or flow_rates[cur_idx] == 0 else [None])
    new_states = []
    
    # debuging = happy_path.pop(0)
    # if debuging in neighbors:
    #     neighbors = [debuging]
    # else:
    #     print(neighbors)
    #     print('', end='')
    
    for move in neighbors:
        new = np.copy(state)
        new[:, 1] += new[:, 0]  # increment cumlative flow rates
        if move is None:  # if we're opening the current valve
            new[cur_idx, 0] = 1  # turn this valve to 'on'
        else:
            new[0, -1] = index_valve[move]  # change current location
        new_states.append(new)
        
        # happy_set.add(new.tobytes())
        
    return new_states



def solve(data, is_part1=True): 
    connections = dict()
    flow_rates = np.zeros(len(data))
    valve2idx = dict()
    
    for idx,info in enumerate(data):
        connections[info[0]] = info[2:]
        connections[idx] = info[2:]  # can use either string or index to determine next nodes
        flow_rates[idx] = info[1]
        valve2idx[info[0]] = idx
    
    state = np.zeros((len(data), 3), dtype=int)  # [valve states, cumlative time open, index of current valve]
    
    def dummy_dist(*args):
        return 1
    
    def dummy_dist_10(*args):
        return 10
    
    def closed_valves(state_vec, _):
        return np.count_nonzero(flow_rates) - np.count_nonzero(state_vec[:, 0])
    
    def no_h(state_vec, _):
        return 0
    
    def digit_pressure(state_vec, _):
        p = np.sum(state_vec[:, 1] * flow_rates)
        return -p/100
    
    max_r = np.sum(flow_rates)
    def flow_rate_left(state_vec, _):
        return max_r - np.sum(state_vec[:, 0] * flow_rates)
    
    # return Astar([connections, flow_rates, valve2idx], state, None, dummy_dist, no_h)
    return Astar([connections, flow_rates, valve2idx], state, None, dummy_dist, flow_rate_left)
    

    return None


# import pickle
# happy_path = ["DD", None, "CC", "BB", None, "AA", "II", "JJ", None, "II", "AA", 
#               "DD", "EE", "FF", "GG", "HH", None, "GG", "FF", "EE", None, "DD", 
#               "CC", None, None, None, None, None, None]
# with open('happy_path.pkl', 'rb') as f:
#     happy_set = pickle.load(f)


test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 1651 )
print(solve(puzz_input))

# print('\n\n' + 'Part 2'.center(50,'-'))
# check( solve(test_case, False), 56000011 )
# print(solve(puzz_input, False))