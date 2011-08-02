"""
Here are my ideas for axes of experimentation
=======
import students
import problem
import random
import exam
import hillclimber
import updater
import math
import sys
import prob_map

LOGISTIC = 0
BINARY = 1
LINEAR = 2

MEAN = 0
PRODUCT = 1
MIN = 2

logistic_diffs = {}
binary_diffs = {}
linear_diffs = {}


def main():

    # Problem set parameters
    num_problems = 1
    concepts = ["IA","IB","II"]
    num_concepts = len(concepts)
    num_answers = 10
    avg_concepts_involved = 1.5
    num_trials = 1
    f = open("inferences.txt", "w")    
    # Initialize student models
    logistic_student = students.LogisticStudent(concepts)    
    binary_student   = students.BinaryStudent(concepts)
    linear_student   = students.LinearStudent(concepts)
    
    my_students = {logistic_student: "Logistic Student", binary_student:  "Binary Student", linear_student:  "Linear Student"}
    problem_set = exam.RandomProblemSet(concepts, num_problems, num_answers, avg_concepts_involved)
>>>>>>> .r223

let the algorithms be

<<<<<<< .mine
LIN-MULT
LIN-MEAN
LIN-MIN
BIN-MULT
BIN-MULT
BIN-MEAN
LOG-MULT
LOG-MULT
LOG-MEAN
=======
        problem_set = exam.RandomProblemSet(concepts, num_problems, num_answers, avg_concepts_involved)
    
        # Answers array:
        answers = []
        answers.append([])
        answers.append([])
        answers.append([])
        answers_index = 0
        
        logistic_student.random_competences()
        competences = logistic_student.competences
        for student in my_students.keys():
            # initialize the competences or the student
            student.competences = competences
            # f.write('\n' + my_students.get(student) + '\n')
            # Record student success on problem set
            for item in problem_set.problems:
                #result = random.random() < student.answer_problem_correctly(item)
                result = random.random() < prob_map.MultMap().process(student.get_prob_correct(item))
                # f.write(str(result) + ", ")
                answers[answers_index].append(result)
            answers_index += 1
>>>>>>> .r223

Number of problems
Number of concepts
Number of concepts per problem

We will:
Generate a set of student results for each problem set

...using each of the 9 models?

Evaluate each set of results with each student model to generate a model

...using each of the 9 models?

That is, are you going to have 81 different combinations (generate
data for each of the 9 models, and see how well that model's
performance is predicted by each of the 9 models?)  Or are you
thinking something different about how to set this up?

see how the guesses are (percentagewise difference)
see average difference between probability of

...?

Graph the performance of each model across increasing number of concepts 1 - 10

   increasing number of problems 10, 50, 100, 500
"""
import prob_map
import exam
import random
import sim_annealing
import students

mult = prob_map.MultMap()
mean = prob_map.MeanMap()
min = prob_map.MinMap()

concepts = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
num_problems = [10, 25, 50, 100]
num_iterations = 1
avg_concepts_involved = 1.5
num_answers = -1
max_concepts = 10
f = open('big_results.txt', 'w')

strategies = {mult: ' mult,', mean: ' mean,', min:' min,'}

for i in range(1, max_concepts + 1):
 cons = concepts[0:i]
 log = students.LogisticStudent(cons)
 bin = students.BinaryStudent(cons)
 lin = students.LinearStudent(cons)
 all_students = {log: ' log,', lin: ' lin,', bin:' bin,'}
 for stu in all_students:
  for strat in strategies:
   for num_p in num_problems:
    for i in range(num_iterations):
     stu.random_competences()
     answers = []
     exm = exam.RandomProblemSet(cons, num_p, num_answers, avg_concepts_involved)
     for item in exm.problems:
      result = random.random() < strat.process(stu.get_prob_correct(item))
      answers.append(result)
     true_comp = stu.get_competences()
     guess = sim_annealing.most_likely_explanation(stu, exm, answers, strat)
     f.write('\n')
     f.write('\n')
     f.write('\n')
     f.write(all_students[stu] + strategies[strat] + str(len(cons)) + ', ' + str(num_p) + '\n')
     f.write(str(exm))
     f.write('\n')
     f.write(str(answers))
     f.write('\n')
     f.write(str(true_comp))
     f.write('\n')
     stu.competences = true_comp
     f.write(str(students.get_probability_of_outcome(exm, answers, stu, strat)))
     f.write('\n')
     f.write(str(guess))
     f.write('\n')
     stu.competences = guess
     f.write(str(students.get_probability_of_outcome(exm, answers, stu, strat)))


f.close()