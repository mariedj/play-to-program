import math

def main():
    f = open("backup.txt", "r")
    lines = []
    for line in f:
        lines.append(line)
    #print lines[0:10]
    start = 0
    while start < len(lines):
        start += 3
        stud, strat, numconcepts, numproblems = lines[start].split(',')
        
        numconcepts = int(numconcepts)
        numproblems = int(numproblems)
        print stud
        print strat
        print numconcepts
        print numproblems        
        #process problems
        start += 3
        problems = exam_process(lines[start])
        #process answers
        start += 1
        answer_line = answer_process(line)
        #process original student
        start += 1
        true_model = get_model(lines[start])
        start += 1
        prob_true_model = float(lines[start])
        #process our guess
        start += 1
        my_model=get_model(lines[start])
        start += 1
        prob_my_model = float(lines[start])
        print 'diff', avg_diff_between(true_model, my_model)
        print "prob my model, prob true model", prob_my_model, '\t', prob_true_model
    f.close()
    
def get_model(line):
    model = {}
    #print line
    line = line.replace('}', '').replace('{', '').replace('\n', '').split(',')
    for item in line:
        concept, ability = item.split(':')
        model[concept] = float(ability)
    #print 'model:', model
    return model




def exam_process(line):
    '''print line
    line = line.replace('\n', '').replace(' ','').replace('Problemdifficulties:', '').split(',Problem')
    print line
    problems = []
    for item in line:
            item = item.split(':')
            item = item[2].strip().replace(',','')
            item = float(item)
            problems.append(item)
    return problems'''
    return {}

def answer_process(line):
    '''
    answer_line = line.replace('[', '').replace(']', '').replace('\n', '').split(', ')
    answers = []
    for item in answer_line:
        if item[0] == 'T':
            answers.append(True)
        else:
            answers.append(False)
    return answers
    '''
    return []

def avg_diff_between(model1, model2):
    num = 0
    sum = 0
    
    for item in model1:
        num += 1
        sum += math.fabs(model1.get(item) - model2.get(item))
    return sum/num


def std_deviation(nums):
    mean = sum(nums)/len(nums)
    
    
def graph(datapointsets):
    pass

main()