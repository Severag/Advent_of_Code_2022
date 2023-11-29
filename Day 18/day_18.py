import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = set(tuple(int(val) for val in line.strip().split(',')) for line in f)
    
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
    steam_points = get_steam_points(data) if not is_part1 else None
    
    total = 0
    
    for point in data:
        adj = list(point)  # adjacent point
        sides = 6
        
        for adj in get_adjacents(point):
            # side doesn't count if it's bordering another lava point or 
            # (for part 2) an air pocket (aka a not-steam, not-lave point)
            # if adj in data or (not is_part1 and adj not in steam_points):
            if adj in data:
                sides -= 1
            elif not is_part1 and adj not in steam_points:
                sides -= 1
        
        total += sides
    
    return total



def get_adjacents(point, limits=None):
    adj = list(point)  # adjacent point
    adjacents = []
    
    for idx in range(3):
        for offset in [-1, 1]:
            adj[idx] += offset
            
            # if we don't care about limits or the new coord is within limits
            if limits is None or (limits[idx][0] <= adj[idx] <= limits[idx][1]):
                adjacents.append(tuple(adj))            
            
            adj[idx] = point[idx]
    
    return adjacents



def get_steam_points(data):    
    all_points = np.array([list(row) for row in data])
    min_pnt = np.min(all_points, axis=0) - 1
    max_pnt = np.max(all_points, axis=0) + 1
    limits = np.array([min_pnt, max_pnt]).T
    
    open_list = [tuple(min_pnt)]
    closed_list = set()  # list of points in the water/steam cloud
    
    while open_list:
        point = open_list.pop()
        
        if point not in closed_list:  # skip if we've been here before
            # otherwise add all adjacent points that aren't lava to open list
            open_list += [adj for adj in get_adjacents(point, limits) if adj not in data]
            
            closed_list.add(point)
    
    return closed_list                
        
            


test_case = read_file('test_case.txt')
test_case2 = read_file('test_case2.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 64 )
check( solve(test_case2), 108 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 58 )
check( solve(test_case2, False), 90 )
print(solve(puzz_input, False))