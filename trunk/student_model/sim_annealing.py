import random
import math
import students

def mkdict(concepts, values):
    ans = {}
    for i, concept in enumerate(concepts):
        ans[concept] = values[i]
    return ans

def most_likely_explanation(test_student, problem_set, student_answers, calculator):
    guess = []
    num_concepts =  test_student.num_concepts
    for i in range(num_concepts):
        guess.append(.5)
    
    test_student.competences = mkdict(test_student.concepts, guess)
    
    guess = simulated_annealing(guess, test_student, problem_set, student_answers, calculator)
    
    return mkdict(test_student.concepts, guess)

def simulated_annealing(guess, test_student, problem_set, student_answers, calculator):
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

def gen_neighbor(guess, temperature):
    neighbor = []
    for competence in guess:
        move = random.randint(-1, 1)
        new_comp = min(1, max(0, competence + temperature * move))
        neighbor.append(new_comp)
    return neighbor
        
def prob_move(e, enew, t):
    distance = math.fabs(e - enew)
    if enew > e:
        return .9
    else:
        return (1 - math.fabs(e-enew)) * (1 - t) + (1 - t)
