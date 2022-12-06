import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = f.readlines()
    
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



def solve_old(data, is_part1=True): 
    from collections import Counter
    ''' 
    use of counter came from: 
    https://www.geeksforgeeks.org/python-program-to-check-if-a-string-contains-all-unique-characters/
    '''
    word = data[0]
    win_len = (4 if is_part1 else 14) - 1
    
    for idx, char in enumerate(word[win_len:], start=win_len):
        window = word[idx - win_len:idx+1]
        freq = Counter(window)  # dictionary of characters and their counts in word
        if len(freq) == len(window):  # if every character has a single entry in freq
            return idx + 1



def solve(data, is_part1=True): 
    word = data[0]
    win_len = (4 if is_part1 else 14) - 1
    
    for idx, char in enumerate(word[win_len:], start=win_len):
        window = set(word[idx - win_len:idx+1])
        if len(window) == win_len + 1:
            return idx + 1

 

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 7 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 19 )
print(solve(puzz_input, False))
