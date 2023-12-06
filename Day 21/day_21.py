import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        data = dict(line_parser(line.strip()) for line in f)
    
    return data



def line_parser(line):
    items = line.split(' ')
    items[0] = items[0].strip(':')  # get rid of trailing ':'
    
    if items[1][0].isdigit():  # monkey just has number
        return [items[0], [float(items[1].strip())]]
    else:
        return [items[0], [items[2], items[1], items[3]]]
    


def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print('\n' + 'ERROR'.center(50,'*'))
        print('Correct answer:')
        print(answer)
        print('Returned answer:')
    else:
        print('Check passed!')
    print(myanswer)



def get_ops_func():
    funcs = [lambda x,y: x + y,
             lambda x,y: x - y,
             lambda x,y: x * y,
             lambda x,y: x / y]
    f_dict = dict(zip(['+','-','*','/'], funcs))
    
    def ops(key, x, y):
        return f_dict[key](x, y)
    
    return ops



def solve(data, is_part1=True):
    import heapq
    ops = get_ops_func()
    
    reverse, end_nodes, ranks = reverse_dict(data)
    
    values = dict()
    open_list = [[-ranks[val], val] for val in end_nodes]
    heapq.heapify(open_list)
    closed_set = set()
    
    while open_list:
        _, node = heapq.heappop(open_list)
        ups = reverse[node]  
        downs = data[node]  # downstream from the source, aka root
        
        if node not in closed_set:
            if len(downs) < 3:  # just-a-number monkey
                val = downs[0]
            else:  # an operations monkey
                # evaluate this monkey's function
                val = ops(downs[0], values[downs[1]], values[downs[2]])
            
            values[node] = val
            [heapq.heappush(open_list, [-ranks[parent], parent]) for parent in ups]
            closed_set.add(node)
    
    if is_part1:
        return values['root']
    else:
        inv = dict(zip(['+','-','*','/'], 
                       ['-','+','/','*']))
        path = path_to_root(reverse, 'humn')[-2::-1]
        
        # value of non-path child of root
        target = values[[val for val in data['root'][1:] if val not in path][0]]
        values[path[0]] = target
        
        for idx,node in enumerate(path[:-1]):
            downs = data[node]
            
            if downs[2] == path[idx+1]:  # if the first argument is on the path
                other = downs[1]
                mult = -1 if downs[0] == '-' else 1
            else:
                other = downs[2]
                mult = 1
            
            values[path[idx+1]] = ops(inv[downs[0]], mult*values[node], values[other])
        
        return values['humn']



def path_to_root(reverse, start):
    open_list = [start]
    visited = []
    
    while open_list:
        node = open_list.pop()
        visited.append(node)
        open_list += reverse[node]
    
    return visited


def reverse_dict(forward):
    reverse = {'root':[]}
    ranks = {'root':0}
    end_nodes = []
    
    open_list = ['root']
    closed_set = set()
    
    while open_list:
        node = open_list.pop()
        edges = forward[node]
        
        if node in closed_set:  # if we've already visited
            continue  # skip this loop
        elif len(edges) < 3:  # just-a-number monkey
            end_nodes.append(node)
        else:  # an operations monkey
            level = ranks[node] + 1
            for down in edges[1:]:  # for each downstream node
                reverse[down] = reverse.get(down, []) + [node]
                open_list.append(down)
                ranks[down] = min(ranks.get(down, level), level)
                
        
        closed_set.add(node)
    
    return reverse, end_nodes, ranks



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 152 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 301 )
print(solve(puzz_input, False))