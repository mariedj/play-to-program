'''
 File-based exam driver
 
 The first command-line argument should be the name of the file containing
 exam information, formatted as described in config_exam. All other arguments
 should be files containing individual students' results. An example command
 line is:
 
    python test_driver.py exam.txt student1.txt student2.txt
    
 The program would create files results_student1.txt and results_student2.txt,
 containing performance data for the respective students.
'''

# system imports
import math
import random
import sys
# project imports
import config_exam
import exam
import problem
import sim_annealing
import students


def main():
    
    if len(sys.argv) < 1:
        # TODO error condition
        pass
    
    exam = config_exam(sys.argv[1])
    
    student_idx = 2
    while student_idx < len(sys.argv):
        # TODO generate student models from files
        pass
        
    # TODO integrating this code with support for performance on
    # multiple concepts will be a bit of work



if __name__ == '__main__':
    main()
