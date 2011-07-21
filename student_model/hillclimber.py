from prob_map import MultMap

def mkdict(concepts, values):
    ans = {}
    for i, concept in enumerate(concepts):
        ans[concept] = values[i]
    return ans

def most_likely_explanation(test_student, problem_set, student_answers):
    guess = []
    num_concepts =  test_student.num_concepts
    for i in range(num_concepts):
        guess.append(.5)
        
    test_student.competences = mkdict(test_student.concepts, guess)
    
    guess = get_outcome(guess, test_student, problem_set, student_answers, .4, num_concepts)
    guess = get_outcome(guess, test_student, problem_set, student_answers, .3, num_concepts)
    guess = get_outcome(guess, test_student, problem_set, student_answers, .2, num_concepts)
    guess = get_outcome(guess, test_student, problem_set, student_answers, .1, num_concepts)
    guess = get_outcome(guess, test_student, problem_set, student_answers, .05, num_concepts)
    guess = get_outcome(guess, test_student, problem_set, student_answers, .01, num_concepts)
    guess = get_outcome(guess, test_student, problem_set, student_answers, .005, num_concepts)
    return guess

def get_outcome(guess, test_student,  problem_set, student_answers, increment, num_concepts):
    # TODO this is all steps; if there are many concepts it should just be a sampling
    steps = get_hillclimbing_steps(num_concepts, [])
    purge(steps, increment, guess)
    #print test_student
    guess_prob = get_probability_of_outcome(problem_set, student_answers, test_student)
    max_prob = guess_prob
    new_guess = guess
    for step in steps:
        temp_guess = generate_guess(step, guess, increment)
        test_student.competences = mkdict(test_student.concepts, temp_guess)
        prob =  get_probability_of_outcome(problem_set, student_answers, test_student)
        #print prob
        if prob > max_prob:
            #print '  ', prob, '    ', max_prob
            max_prob = prob
            new_guess = temp_guess
    if new_guess == guess:
        #print guess
        return guess
    else:
        return get_outcome(new_guess, test_student, problem_set, student_answers, increment, num_concepts)

def generate_guess(step, old_competence, increment):
    new_competence = []
    for i in range(len(step)):

        comp = old_competence[i] + step[i] * increment
        if comp < 0:
            comp = 0
        if comp > 1:
            comp = 1
        new_competence.append(comp)

    return new_competence
        

def purge(steps, increment, guess):
    ineligible = -2
 
    for i in range(len(guess)):
        if guess[i] - increment < 0:
            ineligible = -1
        if guess[i] + increment > 1:
            ineligible = 1
 
        for step in steps:
            if step[i] == ineligible:
 
                steps.remove(step)
 
            
def get_probability_of_outcome(problem_set,  student_answers, student_model):
    map = MultMap()
    current_prob = 1 * (1.5 ** len(problem_set.problems))
    # this factor is just here to keep the numbers from getting so  small that I
    # start to worry a lot about floaring point precision
    for i in range(len(problem_set.problems)):
        prob_correct = map.process(student_model.get_prob_correct(problem_set.problems[i]))
        #prob_correct = student_model.answer_problem_correctly(problem_set.problems[i])
        if student_answers[i] == True:
            current_prob *= prob_correct
            
        else:
            current_prob *= (1 - prob_correct)
            
    return current_prob


def get_probability_of_answer(problem,  answer, student_model):

    prob_correct = student_model.answer_problem_correctly(problem)
    if answer == True:
        return prob_correct
    else:
        return (1 - prob_correct)
    


def get_hillclimbing_steps(num_concepts, the_list):
    if num_concepts <= 0:
        return the_list
    if len(the_list) == 0:
        newlist = []
        for i in range(-1, 2):  
            (newlist.append([i]))
    else:
        newlist = []
        for item in the_list:
            for i in range(-1, 2):
                temp = []
                for num in item:
                    temp.append(num)
                temp.append(i)
                newlist.append(temp)
    return get_hillclimbing_steps(num_concepts - 1, newlist)
