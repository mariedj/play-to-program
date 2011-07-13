import students
import problem
import random
import exam
import hillclimber
import updater
import math

LOGISTIC = 0
BINARY = 1
LINEAR = 2

MEAN = 0
PRODUCT = 1
MIN = 2

def main():

     
    # Problem set parameters
    num_problems = 500
    num_concepts = 3
    num_answers = 10
    avg_concepts_involved = 1.5
    
    # Initialize student models
    logistic_student = students._logistic_student(num_concepts)    
    binary_student   = students._binary_student(num_concepts)
    linear_student   = students._linear_student(num_concepts)
    
    my_students = {logistic_student: "_logistic _student", binary_student:  "_binary _student", linear_student:  "_linear _student"}
    problem_set = exam._problem_set(num_problems, num_concepts, num_answers, avg_concepts_involved)
    
    # Answers array:
    answers = []
    answers.append([])
    answers.append([])
    answers.append([])
    answers_index = 0
    
    
    # Generate test results.
    f = open("exam_results.txt", "w")
    f.write("\nnum_problems = " + str(num_problems) +
            "\nnum_concepts = " + str(num_concepts) +
            "\nnum_answers = "  + str(num_answers) + "\n")
    
    for student in my_students.keys():
        # initialize the competences or the student
        student.random_competences()
        f.write('\n' + my_students.get(student) + '\n')
        
        # Record student success on problem set
        for item in problem_set.problems:
            result = random.random() < student.answer_problem_correctly(item)
            f.write(str(result) + ", ")
            answers[answers_index].append(result)
        answers_index += 1
    
    f.close()


    
    # What we know: All priors are the same. So we just want to find the student parameters
    # that have the highest possibilty of creating our evidence. Later we can adjust this to
    # account for the fact that some settings are more likely than others. Suppose we have
    # full information about the problem difficulties.
    
    f = open("inferences.txt", "w")
    avg_log = 0
    avg_lin = 0
    avg_bnr = 0
    for i in range(100):
        log, lin, bnr = run_tests(f, num_concepts, logistic_student, binary_student, linear_student, problem_set, answers)
        avg_log += sum(log)
        avg_lin += sum(lin)
        avg_bnr += sum(bnr)
    print 'log', avg_log / 300
    print 'lin', avg_lin / 300
    print 'bnr', avg_bnr / 300
    f.close()


    # Now we want to get the model to update in real time.  Let's do this interactively!
    p = problem._problem(num_concepts, num_answers, avg_concepts_involved)
    logistic_guess = [.5, .5, .5]
    binary_guess = [.5, .5, .5]
    linear_guess = [.5, .5, .5]
    
    print "_estimated _logistic _competence _level:\n" + str(logistic_guess)
    print "_estimated _binary _competence _level:\n" + str(binary_guess)
    print "_estimated _linear _competence _level:\n" + str(linear_guess)
    print p


    #interactive sessions are fun!
    # this explores how updating could work
    while raw_input("_answer _question(y/n):   ")[0] == 'y':
        answer = (raw_input("_correctly (y/n)"  )[0] == 'y')
        # update logistic model
        temp_stud = (students._logistic_student(num_concepts))
        temp_stud.set_competences(logistic_guess)
        logistic_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        # update binary model
        temp_stud = (students._binary_student(num_concepts))
        temp_stud.set_competences(binary_guess)
        binary_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        # update linear model
        temp_stud = (students._linear_student(num_concepts))
        temp_stud.set_competences(linear_guess)
        linear_guess = updater.update_model(temp_stud, p, answer, num_concepts)
        print "_estimated _logistic _competence _level:\n" + str(logistic_guess)
        print "_estimated _binary _competence _level:\n" + str(binary_guess)
        print "_estimated _linear _competence _level:\n" + str(linear_guess)
        p = problem._problem(num_concepts, num_answers, avg_concepts_involved)
        print p
    


def run_tests(f, num_concepts, logistic_student, binary_student, linear_student, problem_set, answers):
    test_student = students._logistic_student(num_concepts)
    test_student.set_competences(logistic_student.competences)
    logistic_guess = hillclimber.most_likely_explanation(test_student, problem_set, answers[LOGISTIC], num_concepts)

    f.write('\n' + '_logistic _student' + '\n')    
    f.write("_actual _competence _level:\n" + str(logistic_student.competences) + "\n")
    f.write("_estimated _competence _level:\n" + str(logistic_guess) + "\n")

    test_student = students._binary_student(num_concepts)
    test_student.set_competences(binary_student.competences)
    binary_guess = hillclimber.most_likely_explanation(test_student, problem_set, answers[BINARY], num_concepts)
    
    f.write('\n' + '_binary _student' + '\n')    
    f.write("_actual _competence _level:\n" + str(binary_student.competences) + "\n")
    f.write("_estimated _competence _level:\n" + str(binary_guess) + "\n")    

    test_student = students._linear_student(num_concepts)
    test_student.set_competences(linear_student.competences)
    linear_guess = hillclimber.most_likely_explanation(test_student, problem_set, answers[LINEAR], num_concepts)
                
    f.write('\n' + '_linear _student' + '\n')    
    f.write("_actual _competence _level:\n" + str(linear_student.competences) + "\n")
    f.write("_estimated _competence _level:\n" + str(linear_guess) + "\n")

    logistic_diffs = []
    binary_diffs = []
    linear_diffs = []

    
    for i in range(num_concepts):
        logistic_diffs.append(math.fabs(logistic_student.competences[i] - logistic_guess[i]))
        binary_diffs.append(math.fabs(binary_student.competences[i] - binary_guess[i]))
        linear_diffs.append(math.fabs(linear_student.competences[i] - linear_guess[i]))
        
    return logistic_diffs, binary_diffs, linear_diffs


# Run the program
main()
