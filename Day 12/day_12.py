import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [list(line.strip()) for line in f]
    
    return np.array(data)



def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print('\n' + 'ERROR'.center(50,'*'))
        print('Correct answer:')
        print(answer)
        print('Returned answer:')
    else:
        print('Check passed!')
    print(myanswer)



def Astar(graph, start, end, dist, heuristic, must_visit={None,}):
    import heapq
    
    gscores = {start:dist(start, start, graph)}
    fscores = {start:heuristic(start, end) + gscores[start]}
    
    open_set = {start}
    open_list = [(fscores[start], start)]
    
    closed_set = set()
    
    neighbors = np.array([[1,0],[0,1],[-1,0],[0,-1]])
    test_visits = must_visit.copy()
    
    # f_state = np.full(graph.shape, 0.0)                       # for debugging
    # f_state[start] = fscores[start]
    
    while open_list and must_visit:
        old_f, current = heapq.heappop(open_list)
        open_set.discard(current)
        if current in closed_set:
            continue
        else:
            closed_set.add(current)
        
        if current == end:
            break
        
        
        for offset in neighbors:
            cand = tuple(current + offset)  # candidate location
            
            # if cand is within bounds
            if 0 <= cand[0] < len(graph) and 0 <= cand[1] < len(graph[0]):
                cand_g = gscores[current] + dist(current, cand, graph)
                cand_f = cand_g + heuristic(cand, end)
                
                # add if new
                # update previous entry if this one is better
                # otherwise skip
                if (cand not in closed_set and cand not in open_set) or (gscores.get(cand, np.inf) > cand_g):
                    heapq.heappush(open_list, (cand_f, cand))
                    open_set.add(cand)
                    
                    gscores[cand] = cand_g
                    fscores[cand] = cand_f
                    # f_state[cand] = cand_f                    # for debugging
                    
                    must_visit.discard(cand)
        # print(f_state, end='')                                # for debugging
        # print(f'  current = {current}', end='\n\n')
    
    if None in must_visit:
        return gscores[end]  # return length of path to the end
    else:
        dists = [gscores[loc] for loc in test_visits]
        return np.min(dists)        



def solve(data, is_part1=True): 
    start = tuple(np.squeeze(np.where(data == 'S')))
    end = tuple(np.squeeze(np.where(data == 'E')))
    
    grid = data.copy()  # copy data
    grid[start] = 'a'  # modify its copy and not itself
    grid[end] = 'z'
    
    if is_part1:
        def hike_dists(a, b, grid):
            height_a, height_b = ord(grid[a]), ord(grid[b])
            if height_b > height_a + 1:
                return np.inf
            else:
                return np.sum(np.abs(np.array(a) - b))
        
        def manhattan_heuristic(a, b):
            return np.sum(np.abs(np.array(a) - b))
        
        return Astar(grid, start, end, hike_dists, manhattan_heuristic)
    
    else:
        start = end
        end = (-1, -1)
        As_list = {tuple(loc) for loc in zip(*np.where(data == 'a'))}
        
        def reverse_hike_dists(a, b, grid):
            height_a, height_b = ord(grid[a]), ord(grid[b])
            if height_a > height_b + 1:
                return np.inf
            else:
                return np.sum(np.abs(np.array(a) - b))
        
        def no_heuristic(a, b):
            return 0
        
        return Astar(grid, start, end, reverse_hike_dists, no_heuristic, must_visit = As_list)



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 31 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 29 )
print(solve(puzz_input, False))


