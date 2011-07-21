import problem

class ProblemSet:
    def __init__(self, concepts):
        self.problems = []
        self.concepts = concepts

    def addProblem(self, problem):
        self.problems.append(problem)

class RandomProblemSet(ProblemSet):
    def __init__(self, concepts, num_problems=0, num_answers=-1, avg_concepts_involved=2):
	ProblemSet.__init__(self, concepts)
	self.addRandomProblems(num_problems, num_answers, avg_concepts_involved)

    def addRandomProblems(self, num_problems, num_answers=-1, avg_concepts_involved=2):
        for i in range(num_problems):
            self.problems.append(problem.RandomProblem(self.concepts, num_answers, avg_concepts_involved))