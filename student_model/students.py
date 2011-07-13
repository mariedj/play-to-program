import math
import random
import problem


class Student:
    ''' Defines a model for a virtual student

    <Description goes here>
    '''

    def __init__(self, num_concepts):
        self.num_concepts = num_concepts
        self.competences = []
        
    def random_competences(self):
        self.competences = []
        for i in range(self.num_concepts):
            self.competences.append(random.random())
            
    def set_competences(self, competences):
        self.competences = competences
        
    def get_competence(self, concept):
        return self.competences[concept]
    
    def answer_problem_correctly(self, problem):
        probs = self.get_prob_correct(problem)
        prob = 1.0
        for pc in probs:
            if pc != -1:
                prob *= pc #TODO extract this into another class/calc
        #TODO commented out the following for simplicity in bugtracking
        #probIncorrect = 1 - probC
        #probC = (1 - (probIncorrect * (1 - problem.accident())))
        return prob

    def get_num_concepts(self):
        return self.num_concepts
    
    def __str__(self):
        r = "Competences\n"
        for concept in self.competences:
            r += str(concept) + " "
        return r


class LogisticStudent(Student):
    ''' Logistic student model.
    
    <Description here>
    '''
    
    def get_prob_correct(self, problem):
        correct = []
        for concept in range(self.get_num_concepts()):
            if problem.get_difficulty(concept) != 0:
                likelihood = self.logistic_fn(problem.get_difficulty(concept),
                    self.get_competence(concept))
                correct.append(likelihood)

        return correct

    def logistic_fn(self, problemDifficulty, competence):
        return 1.0 / (1 + math.exp(-16 * (competence + .1 - problemDifficulty)))


class LinearStudent(Student):
    ''' Linear student model.

    Success probability is determined by a linear function
    '''

    def get_prob_correct(self, problem):
        correct = []
        for concept in range(self.num_concepts):
            if self.get_competence(concept) != 1:
                likelihood = (problem.get_difficulty(concept) - 1) / \
                              (self.get_competence(concept) - 1)
                if likelihood > 1:
                    # if d < c then p(corr) > 1 -- we cap at 1
                    likelihood = 1
                correct.append(likelihood)
        return correct


class BinaryStudent(Student):
    ''' Binary student model.
    
    Gives 1.0 probability for a concept if the student's competence matches
    or exceeds the difficulty rating, and .05 if it does not.
    
    Returns a list containing the success probability for each concept, in
    order.
    '''
    
    def get_prob_correct(self, problem):
        correct = []
        for concept in range(self.num_concepts):
            if self.get_competence(concept) < problem.get_difficulty(concept):
                correct.append(0.1)
            elif problem.get_difficulty(concept) > 0:
                correct.append(1)
        
        return correct
