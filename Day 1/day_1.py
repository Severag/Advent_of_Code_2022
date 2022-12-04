import os, math
import numpy as np
# pdb.set_trace()

__location__ = os.path.dirname(__file__)


def read_file(filename):
    # import ast
    # with open( os.path.join(__location__, filename), 'r') as f:
        # data = list(map( ast.literal_eval, f))
    
    with open( os.path.join(__location__, filename), 'r') as f:
        data = [line.strip() for line in f]
    
    return data
    


def check(myanswer, answer):
    if False in (myanswer == answer):
        print('\n' + 'ERROR'.center(50,'*'))
        print('Correct answer:')
        print(answer)
        print('Returned answer:')
    else:
        print('Check passed!')
    print(myanswer)
    


def solve(data, is_part2=False): 
        
    elves = []
    idx = 0
    for item in data:
        if idx >= len(elves):
            elves.append(0)
        
        if item == '':
            idx += 1
        else:
            elves[idx] += int(item)
        
    if not is_part2:    
        return np.array( [max(elves),] )
    else:
        top3 = np.sort(elves)[-3:]
        return np.array( [sum(top3),] )
    
    
    

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), np.array( [24000,] ) )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, True), np.array( [45000, ] ) )
print(solve(puzz_input, True))