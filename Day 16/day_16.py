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



def Astar(info, start, end, dist, heuristic, is_part1):
    import heapq
    # connections, flow_rates, valve2idx
    connections, flow_rates, index_valve = info
    
    gscores = {start.tobytes():0}
    fscores = {start.tobytes():heuristic(start, end) + 0}
    
    open_set = {start.tobytes()}
    open_list = [(fscores[start.tobytes()], 0, start.tobytes())]  # (cost, (-)cumlative pressure released, state)
    
    closed_set = set()
    
    max_r = np.sum(flow_rates)
    best = [0, start]
    
    links = dict()
    end_time = 30 if is_part1 else 26
    
    while open_list:
        old_f, old_flow, current_bytes = heapq.heappop(open_list)
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
            time_left = end_time - gscores[current_bytes]
            # if this path can't exceed the current best, even with max flow rate
            # for the rest of the time, don't bother propagating it anymore
            if best[0] > np.abs(old_flow) + time_left * max_r:
                continue
        
        
        # if current has opened all the valves
        if np.count_nonzero(flow_rates) - np.count_nonzero(current[:, 0]) == 0:
            # don't produce more children, just propagate forward
            current[:, 1] += current[:, 0]
            candidates = [[current, gscores[current_bytes] + 1]]
        else:
            candidates = get_new_states(current, connections[cur_node_num], gscores[current_bytes], flow_rates)
        
        
        for cand,new_time in candidates:
            cand_bytes = cand.tobytes()
            cand_g = new_time
            cand_f = cand_g + heuristic(cand, end)
            
            # add if new
            # update previous entry if this one is better
            # otherwise skip
            if (cand_bytes not in closed_set and cand_bytes not in open_set) or (
                                   gscores.get(cand_bytes, np.inf) > cand_g):
                heapq.heappush(open_list, (cand_f, -total_flow(cand, flow_rates), cand_bytes))
                open_set.add(cand_bytes)
                
                gscores[cand_bytes] = cand_g
                fscores[cand_bytes] = cand_f
                links[cand_bytes] = current_bytes
    
    
    return best[0]



def total_flow(state, flow_rates):
    return np.sum(state[:, 1] * flow_rates)



def get_new_states(state, neighbors, current_time, flow_rates, is_part1):
    # assume the current valve has already been turned on
    end_time = 30 if is_part1 else 26
    new_states = []
    for new_node, dist in neighbors:
        # only go to valves that haven't been opened yet, and that aren't too far in the future
        if state[new_node, 0] == 0 and dist + 1 + current_time <= end_time:
            new = np.copy(state)
            new[:, 1] += new[:, 0] * (dist + 1)  # increment cumlative flow rates
                                                 # +1 is extra minute to turn valve on
            new[0, 2] = new_node                 # change current location
            new[new_node, 0] = 1                 # turned valve on
            new_states.append([new, current_time + dist + 1])
    
    if not new_states:  # if we couldn't find any valid moves
        # just propagate to the end    
        new = np.copy(state)
        new[:, 1] += new[:, 0] * (end_time - current_time)  # increment cumlative flow rates
        new_states.append([new, end_time])
    
    return new_states



def nonzero_connections(node_dict, flow_rates, start):
    nonzeros = np.where(flow_rates > 0)
    
    nz_conns = dict()
    for node in np.append([start], nonzeros[0]):
        dists = spfa(node_dict, node).astype(int)
        nz_conns[node] = [[this_node, others] for this_node, others in 
                         zip(nonzeros[0], dists[nonzeros]) if this_node != node]
    
    return nz_conns



# shortest path faster algorithm
def spfa(conn, start):
    '''
    conn : dictionary
        keys are node names, values are its neighboring nodes
    start : int
        a key in conn for the first node
    '''
    
    dists = np.full(len(conn), np.inf)
    dists[start] = 0
    
    from collections import deque
    open_list = deque()
    open_list.append(start)
    
    closed_set = set()
    
    while open_list:
        current = open_list.popleft()
        closed_set.add(current)
        
        # check all of its neighbors
        marginal_dist = 1
        for neighbor in conn[current]:
            new_dist = dists[current] + marginal_dist
            if dists[neighbor] > new_dist:
                dists[neighbor] = new_dist
                
                if neighbor not in open_list and neighbor not in closed_set:
                    open_list.append(neighbor)
    return dists



def solve(data, is_part1=True): 
    connections = dict()
    flow_rates = np.zeros(len(data))
    valve2idx = dict()
    
    for idx,info in enumerate(data):
        connections[info[0]] = info[2:]
        connections[idx] = info[2:]  # can use either string or index to determine next nodes
        flow_rates[idx] = info[1]
        valve2idx[info[0]] = idx
    
    start = valve2idx['AA']
    
    int_conn = dict()
    for key,conn_nodes in connections.items():
        if isinstance(key, int):
            int_conn[key] = [valve2idx[val] for val in conn_nodes]    
    
    # gives minutes in between all valves with nonzero flow rates
    # so we don't have to care about the 0-value valves
    nz_conns = nonzero_connections(int_conn, flow_rates, start)
    
    state = np.zeros((len(data), 3), dtype=int)  # [valve states, cumlative time open, index of current valve]
    state[0, 2] = start  # first node is AA, not the first line
    
    def dummy_dist(*args):
        return 1
    
    def no_h(state_vec, _):
        return 0
    
    return Astar([nz_conns, flow_rates, valve2idx], state, None, dummy_dist, no_h, is_part1)
            


test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 1651 )
print(solve(puzz_input))

# print('\n\n' + 'Part 2'.center(50,'-'))
# check( solve(test_case, False), 56000011 )
# print(solve(puzz_input, False))