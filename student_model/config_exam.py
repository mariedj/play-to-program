# this file is meant to read in a config file and return a new exam object
# config file format:
# First non-commented line:
# num_concepts (an int)
# after this there are as many lines as there are problems in the format
# float,float, ..... float and then an int representing num answer choices 
# if a problem is not multiple choice, set the num answer choices to -1
# an example might look like this
# # Midterm 2
# 4,t
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

    exam_info = lines[0]
    exam = lines[1:]
    num_concepts = int(exam_info[0].strip())

    problems = []
    for line in exam:
        num_answers = int(line[-1].strip())
        concepts = []
        for i in xrange(num_concepts):
            concepts.append[float(line[i].strip())]
        p = Problem.problem(num_concepts, num_answers, 0)
        p.set_attributes(concepts)
        problems.append(p)
    e = exam.Exam(0,0,0,0)
    e.setProblems(problems)
    return e
