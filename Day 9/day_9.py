import numpy as np

def read_file(filename):
    def parse_line(line):
        terms = line.strip().split(' ')
        return terms[0], int(terms[1])
    
    with open( filename, 'r') as f:
        data = [parse_line(line) for line in f.readlines()]
    
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
    vectors = {'R':[0,1], 'L':[0,-1], 'U':[1,0], 'D':[-1,0], }    
    rope = [[np.array([0,0])] for _ in range(2 if is_part1 else 10)]
    
    for direc, mag in data:
        for idx in range(mag):
            hnew = rope[0][-1] + vectors[direc]
            rope[0].append(hnew)
            
            for idx,locs in enumerate(rope[1:], start=1):
                delta = rope[idx-1][-1] - locs[-1]
                if np.max(np.abs(delta)) >= 2:  # if the tail needs to move
                    # normalize delta to move max of 1 in any direction
                    mask = np.abs(delta) > 0
                    delta[mask] = delta[mask] / np.abs(delta[mask])
                    # delta = np.divide(delta, np.abs(delta), where=delta != 0, out=np.zeros_like(delta))
                    locs.append(locs[-1] + delta)
                else:
                    locs.append(np.array(locs[-1]))
    
    return len(np.unique(rope[-1], axis=0))



test_case = read_file('test_case.txt')
test_case2 = read_file('test_case2.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 13 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 1 )
check( solve(test_case2, False), 36 )
print(solve(puzz_input, False))
