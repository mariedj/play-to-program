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

logistic_diffs = []
binary_diffs = []
linear_diffs = []


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

    # Generate test results.
    #f = open("exam_results.txt", "w")
    f.write("\nnum_problems = " + str(num_problems) +
            "\nnum_concepts = " + str(num_concepts) +
            "\nnumAnswers = "  + str(num_answers) + "\n")
    for i in range(num_trials):

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




        # What we know: All priors are the same. So we just want to find the student parameters
        # that have the highest possibilty of creating our evidence. Later we can adjust this to
        # account for the fact that some settings are more likely than others. Suppose we have
        # full information about the problem difficulties.

        avg_log = 0
        avg_lin = 0
        avg_bnr = 0
        for i in range(1):
            log, lin, bnr = run_tests(f, logistic_student, binary_student, linear_student, problem_set, answers)
            avg_log += sum(log)
            avg_lin += sum(lin)
            avg_bnr += sum(bnr)
        
    print 'log', avg_log / (num_trials * num_concepts)
    print 'lin', avg_lin / (num_trials * num_concepts)
    print 'bnr', avg_bnr / (num_trials * num_concepts)
    f.close()



def run_tests(f, logistic_student, binary_student, linear_student, problem_set, answers):

    concepts = logistic_student.concepts
    test_student = students.LogisticStudent(concepts)
    test_student.competences = logistic_student.competences

    logistic_guess = hillclimber.most_likely_explanation(test_student, problem_set, answers[LOGISTIC])

    f.write('\n' + 'Logistic Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(logistic_student.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(logistic_guess) + "\n")
    
    #prob_model = get_probability_of_outcome(problem_set,  student_answers, logistic_student)
    #guess_student = student.LogisticStudent(logistic_guess)
    #prob_guess = hillclimber.get_probability_of_outcome(problem_set, student_answers, guess_student)
    #print prob_guess/prob_model

    test_student = students.BinaryStudent(concepts)
    test_student.competences = binary_student.competences
    binary_guess = hillclimber.most_likely_explanation(test_student, problem_set, answers[BINARY])
    
    f.write('\n' + 'Binary Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(binary_student.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(binary_guess) + "\n")    

    test_student = students.LinearStudent(concepts)
    test_student.competences = linear_student.competences
    linear_guess = hillclimber.most_likely_explanation(test_student, problem_set, answers[LINEAR])
                
    f.write('\n' + 'Linear Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(linear_student.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(linear_guess) + "\n")

    
    for i, concept in enumerate(concepts): # TODO convert hillclimber to named concepts
        logistic_diffs.append(math.fabs(logistic_student.competences[concept] - logistic_guess[i]))
        binary_diffs.append(math.fabs(binary_student.competences[concept] - binary_guess[i]))
        linear_diffs.append(math.fabs(linear_student.competences[concept] - linear_guess[i]))
        
    return logistic_diffs, binary_diffs, linear_diffs


# Run the program
main()
