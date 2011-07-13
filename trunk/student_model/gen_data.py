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
    numProblems = 500
    numConcepts = 3
    numAnswers = 10
    avgConceptsInvolved = 1.5
    
    # Initialize student models
    logisticStudent = students.LogisticStudent(numConcepts)    
    binaryStudent   = students.BinaryStudent(numConcepts)
    linearStudent   = students.LinearStudent(numConcepts)
    
    myStudents = {logisticStudent: "Logistic Student", binaryStudent:  "Binary Student", linearStudent:  "Linear Student"}
    problemSet = exam.ProblemSet(numProblems, numConcepts, numAnswers, avgConceptsInvolved)
    
    # Answers array:
    answers = []
    answers.append([])
    answers.append([])
    answers.append([])
    answersIndex = 0
    
    
    # Generate test results.
    f = open("examResults.txt", "w")
    f.write("\nnumProblems = " + str(numProblems) +
            "\nnumConcepts = " + str(numConcepts) +
            "\nnumAnswers = "  + str(numAnswers) + "\n")
    
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
    
    log, lin, bnr = run_tests(f, numConcepts, logisticStudent, binaryStudent, linearStudent, problemSet, answers)
    avg_log += sum(log)
    avg_lin += sum(lin)
    avg_bnr += sum(bnr)
    print 'log', avg_log / num_concepts
    print 'lin', avg_lin / num_concepts
    print 'bnr', avg_bnr / num_concepts
    f.close()



def run_tests(f, numConcepts, logisticStudent, binaryStudent, linearStudent, problemSet, answers):
    test_student = students.LogisticStudent(numConcepts)
    test_student.set_competences(logisticStudent.competences)
    logistic_guess = hillclimber.most_likely_explanation(test_student, problemSet, answers[LOGISTIC], numConcepts)

    f.write('\n' + 'Logistic Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(logisticStudent.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(logistic_guess) + "\n")

    testStudent = students.BinaryStudent(numConcepts)
    test_student.set_competences(binaryStudent.competences)
    binary_guess = hillclimber.most_likely_explanation(test_student, problemSet, answers[BINARY], numConcepts)
    
    f.write('\n' + 'Binary Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(binaryStudent.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(binary_guess) + "\n")    

    testStudent = students.LinearStudent(numConcepts)
    test_student.set_competences(linearStudent.competences)
    linear_guess = hillclimber.most_likely_explanation(test_student, problemSet, answers[LINEAR], numConcepts)
                
    f.write('\n' + 'Linear Student' + '\n')    
    f.write("Actual Competence Level:\n" + str(linearStudent.competences) + "\n")
    f.write("Estimated Competence Level:\n" + str(linear_guess) + "\n")

    logistic_diffs = []
    binary_diffs = []
    linear_diffs = []

    
    for i in range(numConcepts):
        logistic_diffs.append(math.fabs(logisticStudent.competences[i] - logistic_guess[i]))
        binary_diffs.append(math.fabs(binaryStudent.competences[i] - binary_guess[i]))
        linear_diffs.append(math.fabs(linearStudent.competences[i] - linear_guess[i]))
        
    return logistic_diffs, binary_diffs, linear_diffs


# Run the program
main()
