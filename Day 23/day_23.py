import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = np.array([np.array(list(line.strip()))  for line in f])
    
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
    locs = list(zip(*np.where(data == '#')))
    new_locs = locs
    steps = [locs]
    
    for idx in range(10 if is_part1 else 100_000):
        old_locs = new_locs
        new_locs = do_turn(new_locs, idx % 4)
        steps.append(new_locs)
        
        # if the elves have already stopped moving, stop the loop
        if new_locs == old_locs:
            print('broke!')
            break
    
    if is_part1:
        pnt_arr = np.array(list(new_locs))
        size = np.max(pnt_arr, axis=0) - np.min(pnt_arr, axis=0) + 1
        
        return np.prod(size) - len(pnt_arr)  # total size - points where elves are
    else:
        return idx + 1  # since idx = 0 calculated the end of step 1



def get_move(point, locs, dir1):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    adjacents = [False] * 4  # are there elves to the [N, S, E, W]
    #                                                  0  1  2  3
    for r in [-1,0,1]:
        for c in [-1, 0, 1]:
            if not r == c == 0 and (point[0] + r, point[1] + c) in locs:
                if r != 0:  # North or South
                    adjacents[(r + 1) // 2] = True  # 0 or 1
                
                if c != 0:  # East or West
                    adjacents[(c + 5) // 2] = True  # 2 or 3
    
    # if we have no adjacents or adjacents in all directions
    if not True in adjacents or not False in adjacents:
        return point  # stay put
    
    # else
    for idx in range(dir1, dir1 + 4):
        idx %= 4  # to start with dir1 and work our way around
        if not adjacents[idx]:  # if there were no adjacents in this direction
            
            return (point[0] + directions[idx][0], point[1] + directions[idx][1])



def do_turn(locs, dir1):
    moves = dict()
    new_locs = set()
    dupes = set()
    
    for point in locs:
        new_point = get_move(point, locs, dir1)
        if new_point in new_locs:  # found a duplicate
            new_locs.add(point)  # it will keep this position
            dupes.add(new_point)  # we'll remove it's entry in new_locs later
        else:
            new_locs.add(new_point)
            moves[new_point] = point  # for use in reset dupes back to their starting point
    
    new_locs -= dupes
    # all the moves in dupes are reset to their previous points
    new_locs |= {moves[new_point] for new_point in dupes}  # merge both sets
    
    return new_locs



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 110 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 20 )
print(solve(puzz_input, False))