import numpy as np

def read_file(filename):
    def parse_line(line):
        terms = line.strip().split(' ')
        return [terms[0], 0 if terms[0] == 'noop' else int(terms[1])]
    
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
    nums0 = [[0,1]] + [[1 if 'noop' in instr else 2, val] for instr, val in data]
    nums = np.cumsum(nums0, axis = 0)
    
    if is_part1:
        spot_checks = np.arange(20, nums[-1, 0], 40, dtype=int)
        output = np.zeros(spot_checks.shape)
        
        for idx, spot in enumerate(spot_checks):
            output[idx] = nums[np.argmax(nums[:, 0] >= spot) - 1, 1]
        
        return np.sum(output * spot_checks)
    else:
        all_indices = np.arange(0, nums[-1,0] + 1, 1, dtype=int)
        all_cycles = np.zeros(all_indices.shape)
        all_cycles[nums[:, 0]] = nums[:, 1]  # copy the values we already have
        indices = np.setdiff1d(all_indices, nums[:, 0])  # the indices we skipped over
        all_cycles[indices] = all_cycles[indices - 1]  # set their values to the rows' before
        
        outstr = ['.'] * nums[-1,0]
        for idx, regis in zip(all_indices, all_cycles):
            if abs(idx % 40 - regis) <= 1:
                outstr[idx] = '#'
        
        return '\n'.join([''.join(row) for row in np.reshape(outstr, (-1, 40))]) + '\n'



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 13140 )
print(solve(puzz_input))

test = '''##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
'''

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), test )
print(solve(puzz_input, False))


