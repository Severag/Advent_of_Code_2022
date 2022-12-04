import os, math
import numpy as np
# pdb.set_trace()

__location__ = os.path.dirname(__file__)


def read_file(filename):
    # import ast
    # with open( os.path.join(__location__, filename), 'r') as f:
        # data = list(map( ast.literal_eval, f))
    
    with open( os.path.join(__location__, filename), 'r') as f:
        data = [line.strip().split(' ') for line in f]
    
    return data
    


def check(myanswer, answer):
    if False in (myanswer == answer):
        print('\n' + 'ERROR'.center(50,'*'))
        print('Correct answer:')
        print(answer)
        print('Returned answer:')
    else:
        print('Check passed!')
    print(myanswer)
    


def solve(data, is_part1=True): 
    result_score = {'loss':0, 'draw':3, 'win':6}
    rps_score = {'rock':1, 'paper':2, 'scissors':3}
    if is_part1:
        translate = dict(zip('ABCXYZ', ['rock', 'paper', 'scissors']*2))
        
        score = 0
        for opponent, me in data:
            outcome = winner(translate[opponent], translate[me])
            score += result_score[outcome]
            score += rps_score[translate[me]]
        
        return np.array( [score,] )
    
    else:
        translate = dict(zip('ABCXYZ', ['rock', 'paper', 'scissors', 'loss', 'draw', 'win']))
        
        score = 0
        for opponent, outcome in data:
            score += result_score[translate[outcome]]
            score += rps_score[get_me(translate[opponent], translate[outcome])]
        
        return np.array( [score,] )
        


def winner(other, me):
    if me in other:
        return 'draw'
    
    if 'rock' in me:
        if 'scissors' in other:
            return 'win'
        else:
            return 'loss'
    elif 'paper' in me:
        if 'rock' in other:
            return 'win'
        else:
            return 'loss'
    elif 'scissors' in me:
        if 'paper' in other:
            return 'win'
        else:
            return 'loss'



def get_me(other, outcome):
    if 'draw' in outcome:
        return other
    
    if 'rock' in other:
        if 'win' in outcome:
            return 'paper'
        else:
            return 'scissors'
    elif 'paper' in other:
        if 'win' in outcome:
            return 'scissors'
        else:
            return 'rock'
    elif 'scissors' in other:
        if 'win' in outcome:
            return 'rock'
        else:
            return 'paper'
    
    

test_case = read_file('test_case.txt')
puzz_input = read_file('puzzle_input.txt')

print('Part 1'.center(50,'-'))
check( solve(test_case), np.array( [15,] ) )
print(solve(puzz_input))

print('\n\n' + 'Part 2'.center(50,'-'))
check( solve(test_case, False), np.array( [12, ] ) )
print(solve(puzz_input, False))