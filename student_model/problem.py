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
        r = "Problem difficulties: "
        for key in self.difficulties:
            r += key + ":" + str(self.difficulties.get(key)) + " "
        return r
        
class RandomProblem(Problem):
    ''' Randomly generate a problem from a list of possible concepts
    '''
    def __init__(self, concepts, num_answers=-1, avg_concepts_involved=2):
        Problem.__init__(self, [], num_answers)
        while not self.concepts:
            for i in range(len(concepts)):
                if random.random() < (float(avg_concepts_involved)/len(concepts)):
                    self.concepts.append(concepts[i])
                    self.difficulties[concepts[i]] = random.random()


# Unit Testing...
def main():
    print '--- Testing Problem'
    prob = Problem(["IA","IB","IC"], 4)
    prob.set_difficulty("IA", 0.25)
    prob.set_difficulty("IB", 0.33)
    prob.set_difficulty("IC", 0.5)
    print prob
    print prob.get_difficulty("IC")
    
    print '--- Testing RandomProblem'
    
    prob = RandomProblem(["IA","IB","IC"], 4, 2)
    print prob
    

if __name__ == '__main__':
    main()
