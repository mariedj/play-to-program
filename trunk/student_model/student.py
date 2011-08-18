'''
 Code for RUR-PLE
'''

from operator import itemgetter

import problems

count = 0

class Concept:
    def __init__(self, name=""):
	self.name = name
        self.att = 0 # attempted
        self.suc = 0 # successful
        self.templates = [] # problem templates
    def __cmp__(self, other):
        c = self.suc * other.att - self.att * other.suc
        if c != 0:
            return c
        if self.att == 0:
            return -1
        if other.att == 0:
            return 1
        return self.att - other.att
    def rate(self): # competence for this concept (correctness rate)
        return float(self.suc) / self.att
    def succ(self): # register one successful attempt involving this concept
        self.att += 1
        self.suc += 1
        if "parent" in self.__dict__ and self.parent.last != count:
            self.parent.last = count
            self.parent.succ()
    def fail(self): # register one failed attempt involving this concept
        self.att += 1
        if "parent" in self.__dict__ and self.parent.last != count:
            self.parent.last = count
            self.parent.fail()


class RW_Concept(Concept): # recency weighted concept tree
    def __init__(self, name=""):
        Concept.__init__(self, name)
        self.rw_att = 10
        self.rw_suc = 3.5
    def __cmp__(self, other):
        return self.rw_suc * other.rw_att - self.rw_att * other.rw_suc
    def rate(self):
        return self.rw_suc / self.rw_att
    def succ(self):
        Concept.succ(self)
        if self.rw_att == 10:
            self.rw_att /= 2
            self.rw_suc /= 2
        self.rw_att += 1
        self.rw_suc += 1
    def fail(self):
        Concept.fail(self)
        if self.rw_att == 10:
            self.rw_att /= 2
            self.rw_suc /= 2
        self.rw_att += 1


"""For this type of student, the problems are selected in a fixed order
that is set during initialization.  It will cycle through the problems once."""
class Student:
    def __init__(self, templates):
        tree = {}
        self.templates = templates
        for plate in templates:
            for concept in plate.concepts:
                if concept in tree:
                    tree[concept].templates.append(plate)
                else:
                    c = Concept(concept)
                    tree[concept] = c
                    c.templates.append(plate)
                    for i in range(-1, -len(concept)-1, -1):
                        if concept[:i] not in tree:
                            p = Concept(concept[:i])
                            tree[concept[:i]] = p
                            c.parent = p
                            p.children = [c]
                            p.last = 0
                            c = p
                        else:
                            p = tree[concept[:i]]
                            c.parent = p
                            p.children.append(c)
                            break
        self.tree = tree
    def next(self):
        if "num" not in self.__dict__:
            self.num = 0
        else:
            self.num += 1
        if self.num != len(self.templates):
            self.last = self.templates[self.num]
        else:
            self.last = None
        global count
        count += 1
        return self.last
    def external(self, prob): # next attempted problem comes from outside
        self.last = prob
        global count
        count += 1
    def succ(self): # successful problem attempt
        for concept in self.last.concepts:
            try:
                self.tree[concept].succ()
            except KeyError:
                pass
    def fail(self): # unsuccessful problem attempt
        for concept in self.last.concepts:
            try:
                self.tree[concept].fail()
            except KeyError:
                pass


"""For this type of student, the next problem is always chosen with
adaptive problem selection based on the current state of the student
model.  The student model is updated with success or failure of any
problem at any time, be it one chosen by next() or an external problem."""
class APS_Student(Student): # student with adaptive problem selection
    def __init__(self, templates):
        tree = {}
        self.templates = templates
        for plate in templates:
            for concept in plate.concepts:
                if concept in tree:
                    tree[concept].templates.append(plate)
                else:
                    c = RW_Concept(concept)
                    tree[concept] = c
                    c.templates.append(plate)
                    for i in range(-1, -len(concept)-1, -1):
                        if concept[:i] not in tree:
                            p = RW_Concept(concept[:i])
                            tree[concept[:i]] = p
                            c.parent = p
                            p.children = [c]
                            p.last = 0
                            c = p
                        else:
                            p = tree[concept[:i]]
                            c.parent = p
                            p.children.append(c)
                            break
        self.tree = tree
        self.previous = [None, None, None]
        self.mastery = 1.0 # competence level needed for mastery
    def next(self):
        self.num = 0
        maxu = 0
        for i, plate in enumerate(self.templates):
            if plate in self.previous:
                continue
            sqsum, sqnum = 0, 0
            for concept in plate.concepts:
                c = self.tree[concept]
                u = self.mastery - c.rate()
                if u < 0:
                    u = 0
                elif c.att >= 2:
                    u *= pow(1 - abs(plate.difficulties[concept] / 10.0 - c.rate()), 2)
                squ = pow(u,2)
                sqsum += squ
                sqnum += 1
                if self.previous[0] and concept in self.previous[0].concepts:
                    sqsum += squ / 2
                    sqnum += 0.5
                if self.previous[1] and concept in self.previous[1].concepts:
                    sqsum += squ / 4
                    sqnum += 0.25
            u = sqsum / sqnum
            if u > maxu:
                maxu = u
                self.num = i
        self.last = self.templates[self.num] if maxu != 0 else None
        self.previous = [self.last, self.previous[0], self.previous[1]]
        global count
        count += 1
        return self.last


"""For this type of student, problems will be selected in a fixed order
that is set on the first call to next().  It will use a ranked order
set by the adaptive problem selection algorithm.  The student model
should be set through success or failure of external problems before
the first call to next().  It will only cycle through the problems once."""
class FPS_Student(APS_Student): # adaptive problem selection sets a fixed order
    def __init__(self, templates):
        APS_Student.__init__(self, templates)
    def rank(self):
        ranks = []
        for i, plate in enumerate(self.templates):
            sqsum, sqnum = 0, 0
            for concept in plate.concepts:
                c = self.tree[concept]
                u = self.mastery - c.rate()
                if u < 0:
                    u = 0
                elif c.att >= 2:
                    u *= pow(1 - abs(plate.difficulties[concept] / 10.0 - c.rate()), 2)
                squ = pow(u,2)
                sqsum += squ
                sqnum += 1
            u = sqsum / sqnum
            ranks.append((i, u))
        ranks.sort(key=itemgetter(1))
        ranks.reverse()
        return ranks
    def next(self):
        if "problemNumber" not in self.__dict__:
            self.num = 0
            self.problemNumber = 0
            self.ranked = self.rank()
        if not self.problemNumber == len(self.templates):
            self.num = self.ranked[self.problemNumber][0]
            self.last = self.templates[self.num]
        else:
            self.last = None
        self.problemNumber += 1
        global count
        count += 1
        return self.last

if __name__ == "__main__":
    import random
    import problem
    probs = [] # TODO: use ProblemSet/exam?
    for prob in problems.tracing:
        new_prob = problem.Problem(prob.concepts)
        for concept in prob.concepts:
            new_prob.set_difficulty(concept, prob.difficulty)
        probs.append(new_prob)
    
    stud = APS_Student(probs)
    for i in range(20):
        prob = stud.next()
        print prob
        if random.random() < 0.5: #TODO: API for probability of prob. correct
            print "correct"
            stud.succ()
        else:
            print "incorrect"
            stud.fail()
# Future work:
# - Implement a problem selection Student class here using the undergrads' new
#   student model
# - Have a virtual student which can learn by doing problems, and can give a
#   probability of getting a problem correct, useful for simulations
# - Run simulations on a virtual student using adaptive problem selection based
#   on my old student model and the new (undergrads') one, to test which
#   results in more learning for the virtual student
# - Implement a similar method of calculating the probability of getting a
#   problem correct based on a modeled student
# - See which student model has better predictive accuracy on actual students'
#   performance on problems from the user study
