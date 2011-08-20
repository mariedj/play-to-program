'''
 Represents an exam problem.
 
 Each Problem object represents a single exam problem, and contains information
 about the exam concepts the problem covers, and the difficulty with which it
 covers each.
'''

import random

class Problem:
    ''' Represents statistical information about a test problem.
    '''
    def __init__(self, concepts, num_answers=-1):
        self.difficulties = {}
        self.concepts = concepts
        self.num_answers = num_answers

    def get_difficulty(self, concept):
        return self.difficulties.get(concept, 0)
        
    def set_difficulty(self, concept, difficulty):
        if difficulty != 0:
            self.difficulties[concept] = difficulty
        
    def __str__(self):
        r = "Problem difficulties: "
        for key in self.difficulties: # TODO change to enumerate?
            r += key + ":" + str(self.difficulties.get(key)) + " "
        return r
        
class RandomProblem(Problem):
    ''' Randomly generate a problem from a list of possible concepts.
    
    
    '''
    def __init__(self, concepts, num_answers=-1, avg_concepts_involved=2):
        Problem.__init__(self, [], num_answers)
        while not self.concepts:
            for conc in concepts:
                # assign random difficulty in random categories
                level = float(avg_concepts_involved)/len(concepts)
                if random.random() < level:
                    self.concepts.append(conc)
                    self.difficulties[conc] = random.random()


#
# Unit Testing
#
def main():
    concepts = ['IA', 'IB', 'IC']
    print '--- Testing Problem'
    prob = Problem(concepts, 4)
    prob.set_difficulty('IA', 0.25)
    prob.set_difficulty('IB', 0.33)
    prob.set_difficulty('IC', 0.5)
    print prob
    print prob.get_difficulty("IC")
    
    print '--- Testing RandomProblem'
    
    prob = RandomProblem(concepts, 4, 2)
    print prob
    
if __name__ == '__main__':
    main()
