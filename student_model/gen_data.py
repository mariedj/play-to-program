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
    concepts = ["IA,IB,II"]
    num_concepts = len(concepts)
    num_answers = 10
    avg_concepts_involved = 1.5
    
    # Initialize student models
    logisticStudent = students.LogisticStudent(concepts)    
    binaryStudent   = students.BinaryStudent(concepts)
    linearStudent   = students.LinearStudent(concepts)
    
    myStudents = {logisticStudent: "Logistic Student", binaryStudent:  "Binary Student", linearStudent:  "Linear Student"}
    problemSet = exam.RandomProblemSet(concepts, num_problems, num_answers, avg_concepts_involved)
    
    # Answers array:
    answers = []
    answers.append([])
    answers.append([])
    answers.append([])
    answersIndex = 0
    
    
    # Generate test results.
    f = open("examResults.txt", "w")
    f.write("\nnum_problems = " + str(num_problems) +
            "\nnum_concepts = " + str(num_concepts) +
            "\nnum_answers = "  + str(num_answers) + "\n")
    
    for student in myStudents.keys():
        # initialize the competences or the student
        student.random_competences()
        f.write('\n' + myStudents.get(student) + '\n')
        
        # Record student success on problem set
        for item in problemSet.problems:
            result = random.random() < student.answerProblemCorrectly(item)
            f.write(str(result) + ", ")
            answers[answersIndex].append(result)
        answersIndex += 1
    
    f.close()


    
    # What we know: All priors are the same. So we just want to find the student parameters
    # that have the highest possibilty of creating our evidence. Later we can adjust this to
    # account for the fact that some settings are more likely than others. Suppose we have
    # full information about the problem difficulties.
    
    f = open("inferences.txt", "w")
    avg_log = 0
    avg_lin = 0
    avg_bnr = 0
    
    log, lin, bnr = run_tests(f, num_concepts, logisticStudent, binaryStudent, linearStudent, problemSet, answers)
    avg_log += sum(log)
    avg_lin += sum(lin)
    avg_bnr += sum(bnr)
    print 'log', avg_log / num_concepts
    print 'lin', avg_lin / num_concepts
    print 'bnr', avg_bnr / num_concepts
    f.close()



def run_tests(f, num_concepts, logisticStudent, binaryStudent, linearStudent, problemSet, answers):
    test_student = students.LogisticStudent(concepts)
    test_student.competences = logisticStudent.competences
    logistic_guess = hillclimber.most_likely_explanation(test_student, problemSet, answers[LOGISTIC], num_concepts)

    f.write('\n' + 'Logistic Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(logisticStudent.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(logistic_guess) + "\n")

    testStudent = students.BinaryStudent(concepts)
    test_student.competences = binaryStudent.competences
    binary_guess = hillclimber.most_likely_explanation(test_student, problemSet, answers[BINARY], num_concepts)
    
    f.write('\n' + 'Binary Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(binaryStudent.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(binary_guess) + "\n")    

    testStudent = students.LinearStudent(concepts)
    test_student.competences = linearStudent.competences
    linear_guess = hillclimber.most_likely_explanation(test_student, problemSet, answers[LINEAR], num_concepts)
                
    f.write('\n' + 'Linear Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(linearStudent.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(linear_guess) + "\n")

    logistic_diffs = {}
    binary_diffs = {}
    linear_diffs = {}

    
    for concept in concepts:
        logistic_diffs[concept] = math.fabs(logisticStudent.competences[concept] - logistic_guess[concept])
        binary_diffs[concept] = math.fabs(binaryStudent.competences[concept] - binary_guess[concept])
        linear_diffs[concept] = math.fabs(linearStudent.competences[concept] - linear_guess[concept])
        
    return logistic_diffs, binary_diffs, linear_diffs


# Run the program
main()
