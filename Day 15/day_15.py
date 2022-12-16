import numpy as np

def read_file(filename):
    def parse_line(line):
        import re
        line = re.split('=|,|:', line)
        # first character may be a negative sign, so isdigit is applied only to the end
        nums = [int(val) for val in line if val[-1].isdigit()]
        return nums
        # return tuple(nums[:2]), tuple(nums[2:])
    
    
    with open( filename, 'r') as f:
        data = [parse_line(line.strip()) for line in f]
    
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



def get_x_range(sensors, radii):
    min_bounds = np.min(sensors.T[0] - radii)
    max_bounds = np.max(sensors.T[0] + radii)
    return np.arange(min_bounds, max_bounds, 1)



def manhattan_dists(A, B):
    dists = np.abs(np.reshape(A, [1,-1,2]) - np.reshape(B, [-1,1,2]))
    return np.sum(dists, axis=2)



def solve(data, is_part1=True): 
    y_cut = 10 if data is test_case else 2_000_000
    sensors, beacons = data[:, :2], data[:, 2:]
    radii = manhattan_dists(beacons, sensors).diagonal().reshape(-1, 1)
        
    if is_part1:
        x_range = get_x_range(sensors, radii)
        points = np.full((x_range.size, 2), y_cut)
        points[:, 0] = x_range
        
        present_beacons = 0
        beacons = np.unique(beacons, axis=0)
        for bcn in beacons:
            # if any bcn coordinates match all the coordinates for a given point
            if np.any(np.all(bcn == points, axis=1)):
                present_beacons += 1
        
        in_range = manhattan_dists(points, sensors) <= radii
        count = np.count_nonzero(np.any(in_range, axis = 0))
        
        return count - present_beacons
    else:
        for sensor_xy, radius in zip(sensors, radii):
            # all valid moves in 1 direction to reach max Manhattan distance
            moves_1D = np.arange(0, radius + 2, 1).reshape(-1, 1)
            #  for [x,y] in these quadrants:       [+,+]  [+,-]  [-,+]  [-,-]
            offsets = np.tile(moves_1D, (1, 8)) * [[1, 1, 1, -1, -1, 1, -1, -1]]
            # reverse the order of every other one, so that the pairs sum to radius + 2
            offsets[:, 1::2] = offsets[::-1, 1::2]  
            # rearrange so that the sets of pairs are stacked atop each other
            offsets = offsets.reshape(-1, 2)
            
            points = sensor_xy + offsets
            # only keep points within bounds
            points = points[np.all((points >= [0,0]) & (points <= [2*y_cut,2*y_cut]), axis=1)]
            
            # distance from each sensor to every point
            dists = manhattan_dists(sensors, points)
            # True iff points is further from every sensor than its corresponding radius
            outta_sensor_range = np.sum(dists <= radii.T, axis=1) < 1
            
            answer = points[outta_sensor_range]
            if len(answer) > 0:  # if we found one
                return np.sum(answer * [[4_000_000.0, 1.]])

        return None
        


test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), 26 )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), 56000011 )
print(solve(puzz_input, False))