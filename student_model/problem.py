import random

class Problem:
    ''' Represents statistical information about a test problem.
    
    <Description goes here>
    '''
    
    def __init__(self, num_concepts, num_answers, avg_concepts_involved):
        # Populate competences vector
        self.difficulties = []
        self.num_concepts = num_concepts
        self.num_answers = num_answers
        for i in xrange(num_concepts):
            if random.random() < (float(avg_concepts_involved)/num_concepts):
                self.difficulties.append(random.random())
            else:
                self.difficulties.append(0)

    def set_attributes(self, difficulties):
        self.difficulties = difficulties
        

    def get_difficulty(self, concept):
        return self.difficulties[concept]
    
    def accident(self):
        #return 1.0/self.numAnswers
        return 0 #TODO change this to another value
        
    def __str__(self):
        r = "Problem difficulties:\n"
        for dif in self.difficulties:
            r += str(dif) + " "
        return r
