"""
This is meant to be a driver for exploring the different models
and seeing what data they generate
It writes to a file called data_gen_driver.txt
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

strategies = {mult: ' mult,', mean: ' mean,', min:' min,'}
f = open('data_gen_driver.txt', 'w')

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