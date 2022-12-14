import numpy as np

def read_file(filename):
    import json
    with open( filename, 'r') as f:
        data = [json.loads(line.strip()) for line in f if len(line) > 2]
    
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



def compare(A, B):
    stack1 = A.copy()
    stack2 = B.copy()
    break_good = False
    break_bad = False
    
    while stack1 and stack2 and not break_good and not break_bad:
        item1 = stack1.pop(0)
        item2 = stack2.pop(0)
        
        if '~' in [item1, item2]:
            break_good = item2 != '~'  # left side ran out of items in this sublist first
            break_bad = item1 != '~'  # right side ran out of items in this sublist first
        elif isinstance(item1, int) and isinstance(item2, int):
            break_good = item1 < item2
            break_bad = item2 < item1
        else:
            if not isinstance(item1, list):
                item1 = [item1]
            
            if not isinstance(item2, list):
                item2 = [item2]
            
            stack1 = item1 + ['~'] + stack1
            stack2 = item2 + ['~'] + stack2
    
    finished_1_early = not stack1 and stack2
    finished_2_early = not stack2 and stack1
    
    if break_good or (not break_bad and finished_1_early):
        return -1  # a < b
    elif break_bad or finished_2_early:
        return 1  # a > b, bad b/c out of order
    else: 
        return 0 



def solve(data, is_part1=True): 
    if is_part1:
        good_packets = []
        
        for idx in range(0, len(data), 2):
            # if the two line are in order or equal
            if compare(data[idx], data[idx+1]) < 1:
                good_packets.append(idx // 2 + 1)
        
        return sum(good_packets)
    else:
        dividers = [[[2]], [[6]]]
        message = dividers + data
        
        from functools import cmp_to_key
        message = sorted(message, key=cmp_to_key(compare))
        
        prod = 1
        for idx, line in enumerate(message, start=1):
            if line in dividers:
                prod *= idx
        
        return prod
        



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 13 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 140 )
print(solve(puzz_input, False))


