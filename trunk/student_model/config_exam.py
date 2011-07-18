# this file is meant to read in a config file and return a new exam object
# config file format:
# First non-commented line:
# concepts (a list of outline section names)
# after this there are as many lines as there are problems in the format
# float,float, ..... float corresponding to difficulties for each concept,
# and then an int representing the number of answer choices 
# if a problem is not multiple choice, set the num answer choices to -1
# an example might look like this
# # Midterm 2
# IA1,IA2,IB,II
# .5,0,0,.9,5
# 0,0,.3,.3,10

import problem
import exam

def get_exam(filename):
    f = open(filename, 'r')
    lines = []
    for line in f:
        if line[0] != '#':
            lines.append(line.split(','))
    f.close()

    concepts = lines[0]
    problems = lines[1:]
    e = exam.ProblemSet(concepts)
    
    for line in problems:
        num_answers = int(line[-1].strip())
        p = Problem.problem(concepts, num_answers)
        for i, concept in enumerate(concepts)):
            p.set_difficulty[concept, float(line[i].strip())]

        e.addProblem(p)

    return e
