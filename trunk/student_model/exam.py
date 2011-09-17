'''
Contains code defining a set of Problems

A ProblemSet is a container class for a group of problems.
'''

import problem

class ProblemSet:
    
    def __init__(self, concepts):
        self.problems = []
        self.concepts = concepts

    def addProblem(self, problem):
        self.problems.append(problem)
        
    def addProblems(self, problems):
        for prob in problems:
            self.problems.append(prob)
        
    def __str__(self):
        st = 'Problem Set\n'
        for i, prob in enumerate(self.problems):
            st += ' ' + str(i) + ': ' + str(prob) + '\n'
        return st
        

class RandomProblemSet(ProblemSet):
    
    def __init__(self, concepts, num_problems=0, num_answers=-1, 
                 avg_concepts_involved=2):
        ProblemSet.__init__(self, concepts)
        self.addRandomProblems(num_problems, num_answers, avg_concepts_involved)

    def addRandomProblems(self, num_problems, num_answers=-1, 
                          avg_concepts_involved=2):
        for i in range(num_problems):
            self.problems.append(problem.RandomProblem(self.concepts, 
                num_answers, avg_concepts_involved))


# Unit testing
def main():
    concepts = ["IA","IB","IC"]
    print '--- Problem Set'
    s = ProblemSet(concepts)
    s.addProblem(problem.RandomProblem(concepts, 4, 2))
    s.addProblem(problem.RandomProblem(concepts, 4, 3))
    print s
    
    print '--- addProblems'
    probs = [problem.RandomProblem(concepts,4,2), problem.RandomProblem(concepts,4,2)]
    s.addProblems(probs)
    print s
    
    print '--- Random Problem Set'
    s = RandomProblemSet(concepts, 3, 4, 2)
    print s


if __name__ == '__main__':
    main();
