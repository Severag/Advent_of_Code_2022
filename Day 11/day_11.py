import numpy as np

def read_file(filename):
    with open( filename, 'r') as f:
        import re
        data = []
        prod = 1
        
        for line in f:
            line_list = re.split(' |,', line.strip().strip(':'))
            
            if 'Monkey' in line:  # start a new monkey
                this_monkey = monkey(int(line_list[-1]))
                data.append(this_monkey)
            
            elif 'Starting' in line:
                this_monkey.items = [int(val) for val in line_list if val.isdigit()]
            
            elif 'Operation' in line:
                this_monkey.term = int(line_list[-1]) if line_list[-1].isdigit() else None
                this_monkey.operand = line_list[-2]
            
            elif 'Test:' in line:
                this_monkey.test_num = int(line_list[-1])
                prod *= this_monkey.test_num
            
            elif 'If true' in line:
                this_monkey.t_num = int(line_list[-1])
            
            elif 'If false' in line:
                this_monkey.f_num = int(line_list[-1])
        
        data2 = [monk.__copy__() for monk in data]  # create duplicates for part 2
        
        for monk1, monk2 in zip(data, data2):
            monk1.set_recipients(data)
            
            monk2.set_recipients(data2)
            monk2.divisor = None  # worries don't reduce by 3 in part 2
            monk2.mod = prod  # to reduce worry to manageable levels w/ modulus division
            # hat tip to Computerphile: https://youtu.be/cbGB__V8MNk?t=565
        
    return [data, data2]



def check(myanswer, answer):
    if not np.array_equal(myanswer, answer):
        print('\n' + 'ERROR'.center(50,'*'))
        print('Correct answer:')
        print(answer)
        print('Returned answer:')
    else:
        print('Check passed!')
    print(myanswer)



class monkey:
    def __init__(self, num):
        self.num = num
        self.inspections = 0
        self.divisor = 3
        self.mod = 0
    
    
    
    def __copy__(self):
        new = monkey(self.num)
        new.items = self.items[:]
        new.test_num = self.test_num
        new.t_num = self.t_num
        new.f_num = self.f_num
        new.term = self.term
        new.operand = self.operand
        new.divisor = self.divisor
        new.mod = self.mod
        
        return new
    
    
    
    def __str__(self):
        return f'{self.num:2d}:\t{self.items}'
    
    
    
    def set_recipients(self, monkey_list):
        self.true_monkey = monkey_list[self.t_num]
        self.false_monkey = monkey_list[self.f_num]
    
    
    
    def play_turn(self):
        while len(self.items) > 0:
            item = self.op(self.items.pop(0))
            self.inspections += 1
            
            if item % self.test_num == 0:
                self.true_monkey.add(item)
            else:
                self.false_monkey.add(item)
    
    
    
    def op(self, item):
        term = item if self.term is None else self.term
        
        if '+' in self.operand:
            result = (item + term) 
        elif '*' in self.operand:
            result = (item * term) 
        
        if self.divisor is not None:
            return result // self.divisor
        else:
            return result % self.mod
    
    
    
    def add(self, item):
        self.items.append(item)
        



def solve(data, is_part1=True): 
    
    for idx in range(20 if is_part1 else 10000):
        for this_monkey in data:
            this_monkey.play_turn()
    
    counts = sorted([this_monkey.inspections for this_monkey in data])
    
    return counts[-2] * counts[-1]



test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case[0]), 10605 )
print(solve(puzz_input[0]))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case[1], False), 2713310158 )
print(solve(puzz_input[1], False))


