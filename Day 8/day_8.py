import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [[int(val) for val in line.strip()] for line in f.readlines()]
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



def get_left_visibility(data):
    isVis = np.full(data.shape, True)
    
    # don't need to check exterior, they're definitionally visible
    # so skip first row and first element in each row
    for r_idx, row in enumerate(data[1:], start=1):
        maxNum = row[0]  # max number in the row so far
        for c_idx, val in enumerate(row[1:], start=1):
            if val <= maxNum:  # if we can't see this tree because a taller one is blocking it
                isVis[r_idx, c_idx] = False
            else:  # we've found a taller tree that subsequent ones can hide behind
                maxNum = val
    
    return isVis



def get_left_score(data):
    scores = np.full(data.shape, 0)
    
    # don't need to check edges, they're definitionally 0
    # so skip first row and first element in each row
    for r_idx, row in enumerate(data[1:-1], start=1):
        for c_idx, val in enumerate(row[1:-1], start=1):
            # work backwards from [r_idx, c_idx] to find a tree of greater or 
            # equal height that'll block the view
            for idx, val2 in enumerate(row[c_idx-1::-1]):
                idx = -idx - 1
                if val2 >= val:
                    break
            scores[r_idx, c_idx] = abs(idx)
    
    return scores



def solve(data, is_part1=True): 
    func = get_left_visibility if is_part1 else get_left_score
    
    left  =  func(data)
    top   =  func(data.T).T
    right =  func(data[:, ::-1])[:, ::-1]
    bottom = func(data[::-1, :].T).T[::-1, :]
    
    if is_part1:
        isVisible = left | top | right | bottom
        return data[isVisible].size
    else:
        return np.max( left * top * right * bottom )

 

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 21 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 8 )
print(solve(puzz_input, False))
