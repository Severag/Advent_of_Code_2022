import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [int(line.strip()) for line in f]
    
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
    nums = len(data)
    arr = np.array([data, np.arange(nums)], dtype=float)
    repeat = 1
    
    if not is_part1:
        arr[0] *= decryption_key
        repeat = 10
    
    for _ in range(repeat):
        for idx in range(nums):
            start = np.where(arr[1] == idx)[0][0]
            end = arr[0, start] + start
            
            if True:
                
                
                while end <= 0 or end >= nums:
                    end = end % nums + end // nums
                    end = nums - 1 if end == 0 else end
                
                if end <= 0 or end >= nums:
                    print('error')
            else:
                while end <= 0:
                    end = end + nums - 1
                while end >= nums:
                    end = end - nums + 1
                
            move_element(arr, int(start), int(end))
    
    start = np.where(arr[0] == 0)[0][0]
    mask = [(val + start) % nums for val in [1000, 2000, 3000]]
    print(arr[0, mask])
    return arr[0, mask].sum(dtype=float)



def move_element(arr, start, end):
    indices_arr = np.arange(len(arr.T))
    temp = [*arr[:, start]]
    arr[:, indices_arr != end] = arr[:, indices_arr != start]
    arr[:, end] = temp



decryption_key = 811589153

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 3 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 1623178306 )
print(solve(puzz_input, False))