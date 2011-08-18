'''
 Exhaustively explores model/combinator combinations.
 
 Generates and tests combinations of {log,lin,bin} students and {mult,mean,min}
 list combinators. Writes results to data_gen_driver.txt
'''

import exam
import prob_map
import random
import sim_annealing
import students

# Combinator maps
mult = prob_map.MultMap()
mean = prob_map.MeanMap()
min = prob_map.MinMap()
strategies = {mult:'mult,', mean:'mean,', min:'min,'}

# Concept names
concepts = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
# Number of problems per exam
num_problems = [10, 25, 50, 100]
# average number of concepts per problem
avg_concepts_involved = 1.5
# free answers
num_answers = -1
# Number of times to run each exam
num_iterations = 1

f = open('data_gen_driver.txt', 'w')

for i in range(1, len(concepts) + 1):  # index 1-10 for print niceness
    print '\nTesting ' + str(i) + ' concepts'
    
    # Select subset of concepts list
    cons = concepts[0:i]
    
    # generative student models
    log = students.LogisticStudent(cons)
    bin = students.BinaryStudent(cons)
    lin = students.LinearStudent(cons)
    all_students = {log: 'log,', lin: 'lin,', bin:'bin,'}
    
    for stu in all_students:
        print 'Testing student: ' + str(stu)
        
        for strat in strategies:
            print 'Testing strategy: ' + str(strat)
            
            for num_p in num_problems:
                print 'Testing ' + str(num_p) + ' problems'
                
                for i in range(num_iterations):
                    stu.random_competences()
                    answers = []
                    exm = exam.RandomProblemSet(cons, num_p, num_answers, \
                                                avg_concepts_involved)
                    for item in exm.problems:
                        result = random.random() < \
                                strat.process(stu.get_prob_correct(item))
                        answers.append(result)
                        
                    true_comp = stu.get_competences()
                    guess = sim_annealing.most_likely_explanation( \
                                                    stu, exm,answers, strat)
                    
                    # print iteration info
                    f.write('\n\n\n')
                    f.write(all_students[stu] + strategies[strat] + \
                            str(len(cons)) + ',' + str(num_p) + '\n')
                    # print exam problems
                    f.write(str(exm))
                    f.write('\n')
                    # print student answers
                    f.write(str(answers))
                    f.write('\n')
                    # print student's real competence
                    f.write(str(true_comp))
                    f.write('\n')
                    # print student's outcome rating given true competence
                    stu.competences = true_comp
                    f.write(str(students.get_probability_of_outcome( \
                            exm, answers, stu, strat)))
                    f.write('\n')
                    # print guessed competence
                    f.write(str(guess))
                    f.write('\n')
                    # print student's outcome rating given guessed competence
                    stu.competences = guess
                    f.write(str(students.get_probability_of_outcome( \
                            exm, answers, stu, strat)))
                    
                # End for - num_iterations
            # End for - num_problems
        # End for - strategies
    # End for - all_students
# End for - concepts

f.close()