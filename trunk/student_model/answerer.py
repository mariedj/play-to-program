def product_answer(student, problem):
    probs = student.get_prob_correct(problem)
    prob = 1.0
    for pc in probs:
        prob *= pc
    return prob

def mean_answer(student, problem):
    probs = student.get_prob_correct(problem)
    prob = 1.0
    for pc in probs:
        prob += pc
    prob /= len(probs)
    return prob

def min_answer(student, problem):
    probs = student.get_prob_correct(problem)
    return min(probs)
