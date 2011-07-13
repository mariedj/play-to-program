from hillclimber import *

import math
def update_model(test_student, new_problem, new_answer, num_concepts):
    guess = test_student.competences
    orig_state = test_student.competences
    guess = update(guess, test_student, new_problem, new_answer, .01, num_concepts, orig_state)
    return guess    


# similarity: otherwise known as 1 - the distance between the vectors
# where the distance is multiplied by some constant
# so we can see some sort of dynamism
# er . . . dynamicness? 
def get_similarity(state_a, state_b):
    diffs = []

    for i in range(len(state_a)):
        diffs.append((state_a[i] - state_b[i]) ** 2)

    return 1 - .0001*math.sqrt(sum(diffs))

def update(guess, test_student, problem, answer, increment, num_concepts, orig_state):
    steps = get_hillclimbing_steps(num_concepts, [])
    purge(steps, increment, guess)
    guess_prob = get_probability_of_answer(problem, answer, test_student)
    max_prob = guess_prob
    new_guess = guess
    for step in steps:
        temp_guess = generate_guess(step, guess, increment)
        test_student.set_competences(temp_guess)
        prob =  get_probability_of_answer(problem, answer, test_student)
        
        prob *= get_similarity(temp_guess, orig_state)
        if prob > max_prob:
            max_prob = prob
            new_guess = temp_guess
    if new_guess == guess:
        #print guess
        return guess
    else:
        return update(new_guess, test_student, problem, answer, increment, num_concepts, orig_state)
