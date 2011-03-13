import string

class Question:
    def __init__(self, instr="", code="", choices=[], correct=0, concepts=[]):
        self.instr = instr
        self.code = code
        self.choices = choices
        self.correct = correct
        self.concepts = concepts
    def check(self):
        if not 'answer' in self.__dict__:
            return False
        if type(self.correct) is type(0):
            return self.correct == self.answer
        corr = [c.strip() for c in self.correct.strip().split()]
        user = [c.strip() for c in self.answer.strip().split()]
        return corr == user

q1 = Question("What is the output of the following code?",
"""grade = 88
if grade >= 70:
    print \"C\"
elif grade >= 80:
    print \"B\"
else:
    print \"A\"
""", ["C", "B", "A", "Nothing because none of the print statements are executed."], 0, ["IA2","IIA1","IIIA1"])

q2 = Question("What is the output of the following code?",
"""temp = 0
if temp < 212:
    print \"water\"
elif temp < 32:
    print \"ice\"
else:
    print \"steam\"
""", ["water", "ice", "steam", "Nothing because none of the print statements are executed."], 0, ["IA2","IIA1","IIIA1"])

q3 = Question("What is the output of the following code?",
"""number = 12
if number % 3 != 0:
    print \"Super\"
else:
    print \"Bowl\"
""", ["Super", "Bowl", "SuperBowl", "There will be no message displayed."], 1, ["IA2","IIA1","IIIA1"])

q4 = Question("What is the output of the following code?",
"""number = 28
if number % 4 == 0:
    print \"Jack\"
else:
    print \"Pot\"
""", ["Jack", "Pot", "JackPot", "There will be no message displayed."], 0, ["IA2","IIA1","IIIA1"])

q5 = Question("""Four lines of code are marked A, B, C, and D with comments.
Which are executed when 45 and 15.00 are entered?""",
"""print \"How many hours did you work? \",
hours = input()
print \"What is your hourly salary? \",
salary = input()

if hours < 0 or salary < 0:
    print \"Invalid entry\" # A
else:
    if hours > 40:
        total = 40 * salary # B
        total = total + (hours - 40) * (salary * 1.5)
    else:
        total = hours * salary # C

    total = total - (0.3 * total) # D
    print \"You earned\", total
""", ["A", "B and D", "B", "C and D", "C", "B, C, and D"], 1, ["IA2","IA3","IIA1","IIA2","IIIA1","IIIA2"])

q6 = Question("""Four lines of code are marked A, B, C, and D with comments.
Which are executed when 35 and 17.00 are entered?""",
"""print \"How many hours did you work? \",
hours = input()
print \"What is your hourly salary? \",
salary = input()

if hours < 0 or salary < 0:
    print \"Invalid entry\" # A
else:
    if hours > 40:
        total = 40 * salary # B
        total = total + (hours - 40) * (salary * 1.5)
    else:
        total = hours * salary # C

    total = total - (0.3 * total) # D
    print \"You earned\", total
""", ["A", "B and D", "B", "C and D", "C", "B, C, and D"], 3, ["IA2","IA3","IIA1","IIA2","IIIA1","IIIA2"])

q7 = Question("What is the value of num after the following code has executed?",
"""num = 11
while num % 2 == 0 and num > 0:
    num = num - 2
""", ["-1", "1", "9", "11"], 3, ["IA1","IA2","IB1a","IIIA1","IIIA2"])

q8 = Question("What is the value of num after the following code has executed?",
"""num = 10
while num % 2 == 0 and num > 0:
    num = num - 2
""", ["0", "8", "9", "10"], 0, ["IA1","IA2","IB1a","IIIA1","IIIA2"])

q9 = Question("How many numbers will be displayed as a result of the following code?",
"""for num in range(10,1,-4):
    print num
""", ["10", "3", "4", "infinitely many"], 1, ["IB2a","IIIB3"])

q10 = Question("How many numbers will be displayed as a result of the following code?",
"""for num in range(3,13,4):
    print num
""", ["10", "3", "4", "infinitely many"], 1, ["IB2a","IIIB3"])

q11 = Question("What is the value of count after the following code has executed?",
"""count = 0
for num in range(2,7):
    if num > 4:
       count = count + num
""", ["18", "15", "11", "0"], 2, ["IA1","IB2a","IB2c","IIA1","IIA2","IIIA1","IIIB2"])

q12 = Question("What is the value of count after the following code has executed?",
"""count = 0
for num in range(2,8):
    if num % 2 == 0:
       count = count + num
""", ["20", "12", "2", "0"], 1, ["IA1","IB2a","IB2c","IIA1","IIA2","IIIA1","IIIB2"])

q13 = Question("What is the output of the following code?",
"""number = 57341
count = 0
while number > 0:
    if number % 10 > 5:
       break
    count += 1
    number /= 10
print count
""", ["0", "1", "3", "5"], 2, ["IA1","IB1a","IB1b","IIA1","IIA2","IIIA1"])

q14 = Question("What is the output of the following code?",
"""number = 85629
count = 0
while number > 0:
    if number % 10 < 5:
       break
    count += 1
    number /= 10
print count
""", ["0", "1", "3", "5"], 1, ["IA1","IB1a","IB1b","IIA1","IIA2","IIIA1"])

q15 = Question("What is the output of the following code?",
"""a = 3 
b = 17

a = b % a
a += 1 
b = a + 5 

print \"a =\", a
print \"b =\", b
""", ["a = 3\nb = 7", "a = 2\nb = 7", "a = 3\nb = 8", "a = 2\nb = 8", "None of the above."], 2, ["IIA1","IIA2"])

q16 = Question("What is the output of the following code?",
"""a = 6
b = 17

b -= 1
a = b % a
b = a * 3 + 5 

print \"a =\", a
print \"b =\", b
""", ["a = 6\nb = 17", "a = 4\nb = 17", "a = 6\nb = 23", "a = 4\nb = 23", "None of the above."], 1, ["IIA1","IIA2"])

q17 = Question("After the following code executes, what value will answer have?",
"""color = 'blue'
shape = 'square'
size = 'small'
answer = -1
if color == 'red':
    answer = 2
elif color == 'blue':
    if shape == 'square':
        if size == 'big':
            answer = 3
        else:
            answer = 5
    else:
        answer = 4
else:
    if size == 'small':
        answer = 6
    else:
        answer = 1
""", ["1", "2", "3", "4", "5", "6"], 4, ["IA2","IA3","IIA1","IIIA1"])

q18 = Question("After the following code executes, what value will answer have?",
"""color = 'yellow'
shape = 'square'
size = 'big'
answer = -1
if color == 'red':
    answer = 2
elif color == 'blue':
    if size == 'small':
        answer = 6
    else:
        answer = 1
else:
    if shape == 'circle':
        answer = 5
    else:
        if size == 'big':
            answer = 4
        else:
            answer = 3
""", ["1", "2", "3", "4", "5", "6"], 3, ["IA2","IA3","IIA1","IIIA1"])

q19 = Question("What is the effect of the following code?",
"""for i in range(1, 16):
    if i % 3 == 0:
        print i
""", ["It prints out the integers from 3 to 15.", "It prints out the multiples of 3 from 3 to 15.", "It prints out the sum of the integers from 3 to 15.", "It prints out the sum of the multiples of 3 from 3 to 15."], 1, ["IA1","IB2a","IB2c","IIIA1","IIIB2"])

q20 = Question("What is the effect of the following code?",
"""for i in range(1, 17):
    if i % 4 == 0:
        print i
""", ["It prints out the integers from 4 to 16.", "It prints out the multiples of 4 from 4 to 16.", "It prints out the sum of the integers from 4 to 16.", "It prints out the sum of the multiples of 4 from 4 to 16."], 1, ["IA1","IB2a","IB2c","IIIA1","IIIB2"])

q21 = Question("What is the output of the following code?",
"""def f(x):
    return 2 * x + 1

def main():
    print f(5), f(f(7))

main()
""", [], "11 31", ["IC","IIB1","IIB2"])

q22 = Question("What is the output of the following code?",
"""def f(x):
    return 3 * x - 1

def main():
    print f(f(4)), f(8)

main()
""", [], "32 23", ["IC","IIB1","IIB2"])

q23 = Question("What is the output of the following code?",
"""x = 1

if x > 3:
    if x > 4:
        print \"A\",
    else:
        print \"B\",
elif x < 2:
    if x != 0:
        print \"C\",

print \"D\"
""", [], "C D", ["IA1","IA2","IA3","IIA1","IIIA1"])

q24 = Question("What is the output of the following code?",
"""y = 5

if y > 4:
    if y < 7:
        print \"U\",
elif y < 3:
    if y == 0:
        print \"M\",
    else:
        print \"B\",

print \"C\"
""", [], "U C", ["IA1","IA2","IA3","IIA1","IIIA1"])

q25 = Question("What is the output of the following code?",
"""n = 1234

while n > 0:
    n /= 10
    print n
""", [], "123\n12\n1\n0", ["IB1a","IIA1","IIA2","IIIA1"])

q26 = Question("What is the output of the following code?",
"""n = 23456

while n > 50:
    n /= 10
    print n
""", [], "2345\n234\n23", ["IB1a","IIA1","IIA2","IIIA1"])

q27 = Question("What is the output of the following code?",
"""for g in range (1, 4):
    for h in range (3):
        if g == h:
            print \"O\",
        else:
            print \"X\",
    print
""", [], "X O X \nX X O \nX X X ", ["IA1","IB2a","IB2c","IB3","IIIA1","IIIB1","IIIB2"])

q28 = Question("What is the output of the following code?",
"""for i in range(1,5):
    for j in range(5):
        if i == j:
            print \"+\",
        else:
            print \"o\",
    print
""", [], "o + o o o \no o + o o \no o o + o \no o o o + ", ["IA1","IB2a","IB2c","IB3","IIIA1","IIIB1","IIIB2"])

q29 = Question("What is the output of the following code?",
"""def f1(a, b):
    print \"f1:\", a, b
    return a

def f2(b, c):
    print \"f2:\", b, c
    return c

def main():
    a = 2
    b = 5
    c = 7

    c = f1(a, b)
    print \"main:\", a, b, c

    b = f2(a, c)
    print \"main:\", a, b, c

main()
""", [], "f1: 2 5\nmain: 2 5 2\nf2: 2 2\nmain: 2 2 2", ["IC","IIA1","IIB1","IIB2"])

q30 = Question("What is the output of the following code?",
"""def f1(a, b):
    print \"f1:\", a, b
    return a

def f2(a, c):
    print \"f2:\", a, c
    return a

def main():
    a = 2
    b = 5
    c = 7

    c = f1(a, b)
    print \"main:\", a, b, c

    a = f2(b, c)
    print \"main:\", a, b, c

main()
""", [], "f1: 2 5\nmain: 2 5 2\nf2: 5 2\nmain: 5 5 2", ["IC","IIA1","IIB1","IIB2"])

q31 = Question("How many times is the loop executed in the following code?",
"""number = 0
while number >= 10:
    number = number - 1
""", ["1", "0", "11", "10"], 1, ["IA1","IA2","IB1a","IIIA1"])

q32 = Question("What is the output of the following code?",
"""a = 4
b = 3
c = 1

if a < b + 1:
    print \"Stop and smell the roses\"
elif a > b + c:
    print \"Type A personality\"
elif a % b >= c:
    print \"What doesn\'t kill me, makes me stronger\"
else:
    print \"I sense a lot of anxiety in this room.\"
""", ["Stop and smell the roses.", "Type A personality.", "What doesn\'t kill me, makes me stronger.", "I sense a lot of anxiety in this room."], 2, ["IA2","IIA1","IIIA1"])

pre = (q1, q3, q5, q7, q9, q11, q13, q15, q17, q19, q21, q23, q25, q27, q29)
post = (q2, q4, q6, q8, q10, q12, q14, q16, q18, q20, q22, q24, q26, q28, q30)
extra = (q31, q32)


if __name__ == '__main__':
    for i, question in enumerate(pre):
        print str(i+1) + ".\t" + question.instr + "\n"
        print question.code
        if len(question.choices) == 0:
            print "#\n"
        else:
            for j, choice in enumerate(question.choices):
                print string.letters[j] + ")\t" + choice
            print
