import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [line.strip() for line in f]
    
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



def parse_line(line):
    components = [txt for txt in line.replace('[',',[,').replace(']', ',],').split(',') if len(txt) > 0]
    
    stack = [[]]
    
    for char in components[1:-1]:
        if char == '[':
            new_list = []
            stack[-1].append(new_list)
            stack.append(new_list)
        elif char == ']':
            stack.pop()
        elif char.isdigit():
            stack[-1].append(int(char))
    
    return stack[0]



def compare(A, B):
    if isinstance(A, int) and isinstance(B, int):
        #     keep checking, is good
        return    A == B,     A < B
    
    # at least a or b is a list, make sure both are
    if not isinstance(A, list):
        A = [A]
    elif not isinstance(B, list):
        B = [B]
    
    # compare the lists term-wise
    for a,b in zip(A, B):
        keepChecking, isGood = compare(a, b)
        
        if not keepChecking:
            return False, isGood  # keepChecking is False here, but to be clearer
    
    # if we made it to the end of one list w/out hitting another criteria
    # check list lengths
    #       keep checking,    is good
    return len(A) == len(B), len(A) < len(B)



def mergesort(data):
    width = len(data)
    
    if width > 1:
        left = mergesort(data[:width//2])
        right = mergesort(data[width//2:])
        
        out = []
        while left and right:
            isEqual, isFirst = compare(left[0], right[0])
            if isEqual or isFirst:
                out.append(left.pop(0))
            else:
                out.append(right.pop(0))
        out += left + right  # add remaining terms leftover in either left or right
        
        return out
    else:
        return data



def solve(data, is_part1=True): 
    if is_part1:
        good_packets = []
        
        for idx in range(0, len(data), 3):
            line1 = parse_line(data[idx])
            line2 = parse_line(data[idx + 1])
            
            isEqual, isGood = compare(line1, line2)
            
            if isEqual or isGood:
                good_packets.append(idx / 3 + 1)
        
        return sum(good_packets)
    else:
        dividers = [[[2]], [[6]]]
        message = dividers + [parse_line(line) for line in data if len(line) > 0]
        
        message = mergesort(message)
        
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


