import problem

class ProblemSet:

    def __init__(self, num_problems, num_concepts, numAnswers, avg_concepts_involved):
        self.problems = []
        for prob in range(num_problems):
            self.problems.append(problem.Problem(num_concepts, numAnswers, avg_concepts_involved))

    def addRandomProblems(self, num_problems, num_concepts, numAnswers, avg_concepts_involved):
        self.problems = []
        for prob in range(num_problems):
            self.problems.append(problem.Problem(num_concepts, numAnswers, avg_concepts_involved))


    def setProblems(self, problems):
        self.problems = problems

    def addProblem(self, problem):
        self.problems.append(problem)
