import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = [line.strip().split(' ') for line in f.readlines()]
    
    system = dict()  # dictionary of dictionaries, for the directories
    current_dir = ''
    
    for idx,line in enumerate(data):
        # if this line is a command
        if line[0] == '$':
            if 'cd' in line:  # if we're moving up, out of a directory
                if line[-1] == '..':
                    # go ahead and calculate its total size
                    size = sum([system[child]['total size'] for child in system[current_dir]['children']
                                if child in system])
                    size += sum([file[0] for file in system[current_dir]['files']])
                    system[current_dir]['total size'] = size
                    
                    # set the new directory
                    new_dir = system[current_dir]['parent']
                
                else:
                    # dive deeper into the file tree
                    new_dir = current_dir + '/' + line[-1]
                
                    if new_dir not in system:  # initialize a new directory in the system
                        if idx > 0 and (current_dir == '' or new_dir not in 
                                        system[current_dir]['children']):
                            print(idx)
                        system[new_dir] = {'parent':current_dir, 
                                           'children':[],
                                           'files':[],
                                           'total size':0}
                current_dir = new_dir
        # if this line is a command output
        else:
            if 'dir' in line:
                system[current_dir]['children'] += [current_dir + '/' + line[-1]]
            else:
                system[current_dir]['files'] += [[int(line[0]), line[1]]]
    
    # manually cd .. our way back to the root node
    while current_dir != '':
        size = sum([system[child]['total size'] for child in system[current_dir]['children']
                    if child in system])
        size += sum([file[0] for file in system[current_dir]['files']])
        system[current_dir]['total size'] = size
        
        # set the new directory
        current_dir = system[current_dir]['parent']
    
    return system
    


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
    sizes = np.array([data[thisdir]['total size'] for thisdir in data.keys()])
    
    if is_part1:
        max_thresh = 100_000
        return np.sum(sizes[sizes <= max_thresh])
    else:
        max_storage = 70_000_000
        req_storage = 30_000_000
        used_storage = data['//']['total size']  # size of root directory
        threshold = req_storage - (max_storage - used_storage)
        sort_size = np.sort(sizes)
        idx = np.where(sort_size >= threshold)[0][0]
        return sort_size[idx]

 

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 95437 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 24933642 )
print(solve(puzz_input, False))
