import random
import math
import students

def most_likely_explanation(test_student, problem_set, student_answers, calculator):
    for concept in test_student.concepts:
        test_student.set_competence(concept, 0.5)
        
    simulated_annealing(test_student, problem_set, student_answers, calculator)
    
    return test_student.competences

def simulated_annealing(test_student, problem_set, student_answers, calculator):
    s = test_student.competences
    e = students.get_probability_of_outcome(problem_set, student_answers, test_student, calculator)
    sbest = {}
    for concept in s:
        sbest[concept] = s[concept]
    ebest = e
    k = 0
    kmax = 2000.0
    while k < kmax:
        temp = k / kmax
        snew = gen_neighbor(s, temp)
        test_student.competences = snew
        enew = students.get_probability_of_outcome(problem_set, student_answers, test_student, calculator)
        if prob_move(e, enew, temp) > random.random():
            s = snew
            e = enew
        if e > ebest:
            sbest = {}
            for concept in s:
                sbest[concept] = s[concept]
            ebest = enew
        k += 1
    #return sbest
    test_student.competences = sbest

def gen_neighbor(guess, temperature):
    neighbor = {}
    for concept in guess:
        move = random.randint(-1, 1)
        new_comp = min(1, max(0, guess[concept] + temperature * move))
        neighbor[concept] = new_comp
    return neighbor
        
def prob_move(e, enew, t):
    distance = math.fabs(e - enew)
    if enew > e:
        return .9
    else:
        return (1 - math.fabs(e-enew)) * (1 - t) + (1 - t)
    
'''    
def update_model(stud, prob, answer, calculator):
    s = guess
    test_student.competences= mkdict(test_student.concepts, s)
    e = students.get_probability_of_outcome(problem_set, student_answers, test_student, calculator)
    sbest = []
    for item in s:
        sbest.append(item)
    ebest = e
    k = 0
    kmax = 2000.0
    while k < kmax:
        temp = k / kmax
        snew = gen_neighbor(s, temp)
        test_student.competences= mkdict(test_student.concepts, snew)
        enew = students.get_probability_of_outcome(problem_set, student_answers, test_student, calculator)
        
        if prob_move(e, enew, temp) > random.random():
            s = snew
            e = enew
        if e > ebest:
            sbest = []
            for item in s:
                sbest.append(item)
            ebest = enew
        k += 1

    return sbest

def gen_updating_neighbor(guess, problem, temperature):
    neighbor = []
    for competence in guess:
        move = random.randint(-1, 1)
        new_comp = min(1, max(0, competence + temperature * move))
        neighbor.append(new_comp)
    return neighbor
    '''