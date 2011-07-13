import students
import problem
import random
import exam
import hillclimber
import updater
import math
import config_exam
import sys

# The first argument is the name of the file containing the exam information.
# Every other argument should be a config file for an individual student's
# results.  So run this as
# python test_driver.py exam.txt student1.txt student2.txt ...
# That call would create the files
# results_student1.txt and results_student2.txt
# for information on how these files should look, please view
# config_exam.py
def main():
    e = config_exam(sys.argv[1])
    student_idx = 2
    while student_idx < len(sys.argv):
        pass
    # TODO integrating this code with support for performance on
    # multiple concepts will be a bit of work




main()
