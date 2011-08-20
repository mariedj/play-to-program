'''
 Convenience function to obtain user exam results.
 
 Reads in a data file and returns a new exam object. The file must be formatted
 as follows:
 
 Comments must contain a hash (#) in the first column of a line; the entire
 line is ignored.
 
 The first non-commented line is a list of the concepts covered in the exam.
 Subsequent lines describe the problems in the exam. Each line represents a
 single question, and contains a CSV list of (float) difficulty ratings
 corresponding to the list of concepts followed by a count (int) of answers
 (for multiple choice problems) or -1 (for non-MC).
 
 A data file might look like:
  ---------------
 | # Midterm 2   |  - commented line
 | IA1,IA2,IB,II |  - list of concept names
 | .5,0,0,.9,5   |  - 5 answer choice MC question, 2/4 concepts covered
 | 0,0,.3,.3,10  |  - 10 answer MC, 2/4 concepts covered
  ---------------
'''

import problem
import exam

def get_exam(filename):
    ''' Reads an exam info file and returns the exam object it describes.
    
    Returns a ProblemSet object containing the contents of the given CSV file.
    '''
    
    # 'lines' is a list of lists, each list containing the CSV contents of one
    # line of the exam info file
    lines = []
    
    # Build data structure 'lines' containing contents of specified file
    f = open(filename, 'r')
    for line in f:
        if line[0] != '#':
            # If not a comment, parse line as CSV and add to 'lines'
            lines.append(line.split(','))
    f.close()
    
    # Build exam object
    concepts = lines[0]
    concepts[-1] = concepts[-1].strip()
    problems = lines[1:]
    
    ex = exam.ProblemSet(concepts)
    
    for line in problems:
        num_answers = int(line[-1].strip()) # answer count is at line end
        del(line[-1])
        p = problem.Problem(concepts, num_answers)
        #print concepts
        #print line
        for i, concept in enumerate(concepts):
            rating = line[i].strip()
            #print concept + ' ' + rating
            p.set_difficulty(concept, float(rating))
        ex.addProblem(p)

    return ex


#
# Unit Testing
#
def main():
    exm = get_exam('sample_ex.txt')
    print exm

if __name__ == '__main__':
    main()
