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



def solve(data, is_part1=True):
    deci_sum = 0
    
    for snaf_num in data:
        deci_sum += snafu_to_decimal(snaf_num)
    
    return decimal_to_snafu(deci_sum)


def snafu_to_decimal(snafu):
    convert = {'2': 2,
               '1': 1,
               '0': 0,
               '-':-1,
               '=':-2}
    decimal = 0
    for idx,val in enumerate(snafu[-1::-1]):
        decimal += convert[val] * 5**idx
    
    return decimal


def decimal_to_snafu(decimal):
    if decimal == 0:
        return 0
    
    digits = []
    rem = 0  # remainder
    while decimal > 0:
        dig = int(decimal % 5)
        
        if dig == 3:
            dig = '='
            rem = 1
        elif dig == 4:
            dig = '-'
            rem = 1
        
        digits.append(str(dig))
        decimal = decimal // 5 + rem
        rem = 0
    
    return ''.join(digits[-1::-1])
    
    

decimal_to_snafu(12345)

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), '2=-1=0' )
print(solve(puzz_input))

# print('\n\n' + 'Part 2'.center(50,'-'))
# check( solve(test_case, False), 54 )
# print(solve(puzz_input, False))