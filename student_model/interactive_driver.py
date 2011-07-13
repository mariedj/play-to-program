import students
import problem
import random
import exam
import hillclimber
import updater
import math

def main():
    num_concepts = 3
    num_answers = -1
    avg_concepts_involved = 2


    # Now we want to get the model to update in real time.  Let's do this interactively!
    p = problem.Problem(num_concepts, num_answers, avg_concepts_involved)
    logistic_guess = [.5, .5, .5]
    binary_guess = [.5, .5, .5]
    linear_guess = [.5, .5, .5]
    
    print "Estimated Logistic Competence Level:\n" + str(logistic_guess)
    print "Estimated Binary Competence Level:\n" + str(binary_guess)
    print "Estimated Linear Competence Level:\n" + str(linear_guess)
    print p


    #interactive sessions are fun!
    # this explores how updating could work
    while raw_input("Answer Question(y/n):   ")[0] == 'y':
        answer = (raw_input("Correctly (y/n)"  )[0] == 'y')
        # update logistic model
        temp_stud = (students.LogisticStudent(num_concepts))
        temp_stud.set_competences(logistic_guess)
        logistic_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        # update binary model
        temp_stud = (students.BinaryStudent(num_concepts))
        temp_stud.set_competences(binary_guess)
        binary_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        # update linear model
        temp_stud = (students.LinearStudent(num_concepts))
        temp_stud.set_competences(linear_guess)
        linear_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        print "Estimated Logistic Competence Level:\n" + str(logistic_guess)
        print "Estimated Binary Competence Level:\n" + str(binary_guess)
        print "Estimated Linear Competence Level:\n" + str(linear_guess)
        p = problem.Problem(num_concepts, num_answers, avg_concepts_involved)
        print p


main()
