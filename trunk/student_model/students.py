import math
import random


class Student:
    ''' Defines a model for a virtual student.
    
    A student model contains a dictionary of concept-competence values ranging
    from 0-1, where each value represents the student's aptitude on the concept
    it corresponds to.
    '''
    def __init__(self, concepts):
        self.concepts = concepts
        self.num_concepts = len(concepts)
        self.competences = {}
        
        for concept in concepts:
            self.competences[concept] = 0.35 #TODO: is that the right value?
        
    def random_competences(self):
        for concept in self.concepts:
            self.competences[concept] = random.random()
            
    def get_competence(self, concept):
        return self.competences[concept]
    
    '''
    This function has been DEPRECATED but is retained for now, just in case
    
    def answer_problem_correctly(self, problem):
        probs = self.get_prob_correct(problem)
        prob = 1.0
        for pc in probs.values():
            if pc != -1:
                prob *= pc #TODO extract this into another class/calc
        #TODO commented out the following for simplicity in bugtracking
        #probIncorrect = 1 - probC
        #probC = (1 - (probIncorrect * (1 - problem.accident())))
        return prob
    ''' 
    
    def get_competences(self):
        my_comps = {}
        for comp in self.competences:
            my_comps[comp] = self.competences.get(comp)
        return my_comps
    
    def set_competence(self, concept, competence):        
        self.competences[concept] = competence           
    
    def __str__(self):
        r = "Competences\n"
        #print self.competences
        for key in self.competences:
            r += key + ":" + str(self.competences.get(key)) + " "
        return r


class LogisticStudent(Student):
    ''' Logistic student model.
    
    <Description here>
    '''
    
    def get_prob_correct(self, problem):
        correct = {}
        #print self.competences
        for concept in self.concepts:
            if problem.get_difficulty(concept) != 0:
                likelihood = self.logistic_fn(problem.get_difficulty(concept),
                    self.get_competence(concept))
                correct[concept] = likelihood

        return correct

    def logistic_fn(self, problemDifficulty, competence):
        return 1.0 / (1 + math.exp(-16 * (competence + .1 - problemDifficulty)))

        
class SoftLogisticStudent(LogisticStudent):
    ''' "Soft" logistic student model.
    
    Same as the logistic student model, but with upper and lower boundaries at
    0.9 and 0.1, respectively, rather than 1.0 and 0.0. This corresponds with
    the chance that a student answers a problem correctly or incorrectly by
    accident.
    '''

    def get_prob_correct(self, problem):
        correct = {}
        for concept in self.concepts:
            if problem.get_difficulty(concept) != 0:
                likelihood = self.logistic_fn(problem.get_difficulty(concept),
                    self.get_competence(concept))
                correct[concept] = likelihood

        return correct

    def logistic_fn(self, problemDifficulty, competence):
        return 0.1 + 0.8 / (1 + math.exp(-16 * (competence + .1 - problemDifficulty)))

        
class LinearStudent(Student):
    ''' Linear student model.

    Success probability is determined by a linear function
    '''

    def get_prob_correct(self, problem):
        correct = {}
        for concept in self.concepts:
            if self.get_competence(concept) != 1:
                likelihood = (problem.get_difficulty(concept) - 1) / \
                              (self.get_competence(concept) - 1)
                if likelihood > 1:
                    # if d < c then p(corr) > 1 -- we cap at 1
                    likelihood = 1.0
                correct[concept] = likelihood
        return correct


class SoftLinearStudent(Student):
    ''' "Soft" linear student model.

    Success probability is determined by a linear function. Upper and lower
    bounds of the function are 0.9 and 0.1, respectively, to reflect the chance
    that a student will answer a question correctly or incorrectly by
    accident.
    '''
    
    def get_prob_correct(self, problem):
        correct = {}
        for concept in self.concepts:
            if self.get_competence(concept) != 1:
                likelihood = (problem.get_difficulty(concept) - 1) / \
                              (self.get_competence(concept) - 1)
                if likelihood > .9:
                    # if d < c then p(corr) > 1 -- we cap at 1
                    likelihood = .9
                if likelihood < .1:
                    # if d < c then p(corr) > 1 -- we cap at 1
                    likelihood = .1
                correct[concept] = likelihood
        return correct
        
        
class BinaryStudent(Student):
    ''' Binary student model.
    
    Gives 1.0 probability for a concept if the student\'s competence matches
    or exceeds the difficulty rating, and .05 if it does not.
    
    Returns a list containing the success probability for each concept, in
    order.
    '''
    
    def get_prob_correct(self, problem):
        correct = {}
        for concept in self.concepts:
            if self.get_competence(concept) < problem.get_difficulty(concept):
                correct[concept] = 0.1
            elif problem.get_difficulty(concept) > 0:
                correct[concept] = .9
        
        return correct
    
    
class SoftBinaryStudent(Student):
    ''' "Soft" binary student model.
    
    Same as the BinaryStudent model, but returns 0.9/0.1 instead of 1/0
    '''
    def get_prob_correct(self, problem):
        correct = {}
        for concept in self.concepts:
            if self.get_competence(concept) < problem.get_difficulty(concept):
                correct[concept] = .1
            elif problem.get_difficulty(concept) > 0:
                correct[concept] = 0.9
        
        return correct


#
# Unit Testing
#
def main():
    import problem
    concepts = ["IA","IB","IC"]
    student1 = SoftBinaryStudent(concepts)
    student2 = SoftLinearStudent(concepts)
    student3 = SoftLogisticStudent(concepts)
    student4 = LinearStudent(concepts)
    student5 = BinaryStudent(concepts)
    student6 = LogisticStudent(concepts)
    p = problem.RandomProblem(concepts, -1, 2)
    
    print p
    print student1.get_prob_correct(p)
    print student2.get_prob_correct(p)
    print student3.get_prob_correct(p)
    print student4.get_prob_correct(p)
    print student5.get_prob_correct(p)
    print student6.get_prob_correct(p)
    
if __name__ == "__main__":
    main()
