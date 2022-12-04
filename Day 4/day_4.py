import numpy as np

def read_file(filename):
    import re
    with open( filename, 'r') as f:
        # data = [line.strip().split(',') for line in f]
        data = [list(map(int, re.split(',|-', line.strip()))) for line in f]
    
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
    overlap = 0
    
    for x1, x2, y1, y2 in data:
        if is_part1:
            if (x1 <= y1 and x2 >= y2) or (
                x1 >= y1 and x2 <= y2):
                overlap += 1
        else:
            if x1 <= y1 <= x2 or y1 <= x1 <= y2:
                overlap += 1
    
    return overlap

 

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 2 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 4 )
print(solve(puzz_input, False))