import random

class Problem:
    ''' Represents statistical information about a test problem.
    '''
    def __init__(self, concepts, num_answers):
        self.difficulties = {}
        self.concepts = concepts
        self.num_answers = num_answers

    def get_difficulty(self, concept):
        return self.difficulties.get(concept, 0)
        
    def set_difficulty(self, concept, difficulty):
        self.difficulties[concept] = difficulty
        if difficulty == 0:
            del self.difficulties[concept]
            self.concepts.remove(concept)
    
    # This function should be deprecated. Accident probabilities should be
    # handled in another class
    def accident(self):
        #return 1.0/self.num_answers
        return 0 #TODO change this to another value
        
    def __str__(self):
        r = "Problem difficulties:\n"
        for key in self.difficulties:
            r += str(key) + ":" + str(self.difficulties.get(key)) + " "
        return r
        
class RandomProblem(Problem):
    ''' Randomly generate a problem from a list of possible concepts
    '''
    def __init__(self, concepts, num_answers, avg_concepts_involved):
        Problem.__init__(self, concepts, num_answers)
        for i in range(len(concepts)):
            if random.random() < (float(avg_concepts_involved)/len(concepts)):
                self.difficulties[concepts[i]] = random.random()
            else:
                self.difficulties[concepts[i]] = 0
            #if random.random() < (float(avg_concepts_involved)/len(concepts)):
            #    self.concepts.append(concepts[i])
            #    self.difficulties[concepts[i]] = random.random()


# Unit Testing...
def main():
    print '--- Testing Problem'
    prob = Problem(3, 4)
    prob.set_difficulty(0, 0.25)
    prob.set_difficulty(1, 0.33)
    prob.set_difficulty(2, 0.5)
    print prob
    print prob.get_difficulty(2)
    
    print '--- Testing RandomProblem'
    
    prob = RandomProblem([0,1,2], 4, 2)
    print prob
    

if __name__ == '__main__':
    main()