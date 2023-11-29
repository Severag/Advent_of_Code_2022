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
    if not is_part1:
        return solve2(data)
    
    total = 0
    
    for point in data:
        adj = list(point)  # adjacent point
        sides = 6
        
        for idx in range(3):
            for offset in [-1, 1]:
                adj[idx] += offset
                
                if tuple(adj) in data:
                    sides -= 1
                
                adj[idx] = point[idx]
        
        total += sides
    
    return total



def solve2(data):
    total = 0
    coords = [set(), set(), set()]
    empties = set()
    
    for point in data:
        adj = list(point)  # adjacent point
        sides = 6
        
        for idx in range(3):
            coords[idx].add(point[idx])
            
            for offset in [-1, 1]:
                adj[idx] += offset
                
                if tuple(adj) in data:
                    sides -= 1
                else:
                    empties.add(tuple(adj))
                
                adj[idx] = point[idx]
        
        total += sides
    
    total -= test_air(empties, data)
    
    return total



def test_air(empties, data):
    is_air = dict(zip(empties, [True]*len(empties)))
    adjacencies = {val:[] for val in empties}
    
    for point in empties:
        adj = list(point)  # adjacent point
        
        for idx in range(3):            
            for offset in [-1, 1]:
                adj[idx] += offset
                this_adj = tuple(adj)
                
                if this_adj in data:
                    pass  # useful to know regardless
                elif this_adj in empties:
                    adjacencies[this_adj].append(point)
                    adjacencies[point].append(this_adj)
                else:  # exposed to water/steam
                    is_air[point] = False
                
                adj[idx] = point[idx]
    
    for point, air_bool in is_air.items():
        if not air_bool:
            open_list = [point]
            closed_list = set()
            
            while len(open_list) > 0:
                pnt = open_list.pop()
                
                if pnt not in closed_list:
                    is_air[pnt] = False  # set pnt's air to be False (borders water space)
                    
                    open_list += adjacencies[pnt]  # check all pnt's adjacent empties
                    
                    closed_list.add(pnt)
    
    air_spaces = set(key for key,val in is_air.items() if val)
    
    return solve(air_spaces)
                
        
            


test_case = read_file('test_case.txt')
test_case2 = read_file('test_case2.txt')
puzz_input = read_file('puzzle_input.txt')

# print('Part 1'.center(50,'-'))
# check( solve(test_case), 64 )
# check( solve(test_case2), 108 )
# print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 58 )
check( solve(test_case2, False), 90 )
# print(solve(puzz_input, False))

# 4240 is too high