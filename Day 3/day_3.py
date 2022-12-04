import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [line.strip().split(' ') for line in f]
    
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
    data = np.squeeze(data)
    import string
    score_dict = dict(zip(string.ascii_lowercase + string.ascii_uppercase, 
                          np.linspace(1, 52, 52, dtype=int)))
    score = 0
    if is_part1:
        for line in data:
            comp1 = set(line[:len(line)//2])
            comp2 = set(line[len(line)//2:])
            
            score += score_dict[(comp1 & comp2).pop()]
    else:
        for idx in range(0, len(data), 3):
            elves = [set(data[idx + offset]) for offset in [0, 1, 2]]
            inter = elves[0] & elves[1] & elves[2]
            score += score_dict[inter.pop()]
        
    return score

 

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 157 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 70 )
print(solve(puzz_input, False))