import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = f.readlines()
    
    # get index where the stacks are labeled
    for lbl_num, line in enumerate(data):
        if '1' in line:
            break
    
    # parse stacks, each in its own list; ie transposed from the file format
    mask = [idx for idx, char in enumerate(data[lbl_num]) if char.isdigit()]
    stacks = []
    for idx in mask:
        # data[lbl_num-1::-1]: work backwards in data to get the bottom of each stack first
        stacks.append( [line[idx] for line in data[lbl_num-1::-1] if line[idx] != ' '] )
        
    instr = []  # instructions
    for line in data[lbl_num+2:]:
        instr.append( [int(word) for word in line.strip().split(' ') if word.isdigit()] )
    
    data = [stacks, instr]
    
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
    state, moves = [[stack[:] for stack in info] for info in data]
    
    for count, source, dest in moves:
        if is_part1:
            for idx in range(count):
                state[dest - 1].append( state[source - 1].pop())
        else:
            state[dest - 1] += state[source - 1][-count:]
            state[source - 1] = state[source - 1][:-count]
    
    answer = ''.join( [spot[-1] for spot in state] )
    
    return answer



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 'CMZ' )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 'MCD' )
print(solve(puzz_input, False))