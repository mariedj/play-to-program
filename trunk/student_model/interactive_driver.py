import students
import problem
import random
import exam
import hillclimber
import updater # TODO what is updater?
import math

def mkdict(concepts, values):
    ans = {}
    for i, concept in enumerate(concepts):
        ans[concept] = values[i]
    return ans

def main():
    concepts = ["IA","IB","II"]
    num_concepts = len(concepts)
    num_answers = -1
    avg_concepts_involved = 2


    # Now we want to get the model to update in real time.  Let's do this interactively!
    p = problem.RandomProblem(concepts, num_answers, avg_concepts_involved)
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
        temp_stud = students.LogisticStudent(concepts)
        temp_stud.competences = mkdict(concepts, logistic_guess)
        logistic_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        # update binary model
        temp_stud = students.BinaryStudent(concepts)
        temp_stud.competences = mkdict(concepts, binary_guess)
        binary_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        # update linear model
        temp_stud = students.LinearStudent(concepts)
        temp_stud.competences = mkdict(concepts, linear_guess)
        linear_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        print "Estimated Logistic Competence Level:\n" + str(logistic_guess)
        print "Estimated Binary Competence Level:\n" + str(binary_guess)
        print "Estimated Linear Competence Level:\n" + str(linear_guess)
        p = problem.RandomProblem(concepts, num_answers, avg_concepts_involved)
        print p


main()
