'''
 Provides an interactive interface to demonstrate student model updating.
 
 Allows the user to simulate a student taking an exam, by allowing them to
 answer 'correct' or 'incorrect' to randomly generated problem difficulties.
 Updates model and displays student results at each iteration.
'''
import exam
import prob_map
import problem
import sim_annealing
import students


def main():
    concepts = ["IA","IB","II"]
    num_answers = -1
    avg_concepts_involved = 2
    
    exm = exam.ProblemSet(concepts)
    answers = []
    
    # Now we want to get the model to update in real time.  Let's do this
    # interactively!
    p = problem.RandomProblem(concepts, num_answers, avg_concepts_involved)
    exm.addProblem(p)
    
    # The initial competence dictionary for all students is initialized to 0.5
    # for all concepts
    start_dic = {}
    for concept in concepts:
        start_dic[concept] = 0.5
    
    logistic_guess = start_dic
    binary_guess = start_dic
    linear_guess = start_dic
    
    print "Estimated Logistic Competence Level:\n" + str(logistic_guess)
    print "Estimated Binary Competence Level:\n" + str(binary_guess)
    print "Estimated Linear Competence Level:\n" + str(linear_guess)
    print p
    
    
    # interactive sessions are fun!
    # this explores how updating could work
    while raw_input("Answer Question? (y/n)  ")[0] == 'y':
        answer = (raw_input("Correctly? (y/n)  ")[0] == 'y')
        answers.append(answer)
        
        # update logistic model
        temp_stud = students.LogisticStudent(concepts)
        temp_stud.competences = logistic_guess
        logistic_guess = sim_annealing.most_likely_explanation( \
                                temp_stud, exm, answers, prob_map.MultMap())
        
        # update binary model
        temp_stud = students.BinaryStudent(concepts)
        temp_stud.competences = binary_guess
        binary_guess = sim_annealing.most_likely_explanation( \
                                temp_stud, exm, answers, prob_map.MultMap())

        # update linear model
        temp_stud = students.LinearStudent(concepts)
        temp_stud.competences = linear_guess
        linear_guess = sim_annealing.most_likely_explanation( \
                                temp_stud, exm, answers, prob_map.MultMap())
        
        print "Estimated Logistic Competence Level:\n" + str(logistic_guess)
        print "Estimated Binary Competence Level:\n" + str(binary_guess)
        print "Estimated Linear Competence Level:\n" + str(linear_guess)
        
        p = problem.RandomProblem(concepts, num_answers, avg_concepts_involved)
        exm.addProblem(p)
        print p


if __name__ == '__main__':
    main()
