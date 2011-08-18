'''
 Code for RUR-PLE
'''

import sys
import random
import environment

if not 'write' in sys.argv:
    writeMode = False
else:
    writeMode = True

def newspaper_fixed():
    #environment(newspaper.wld)
    # IA1 and IB2a
    return (environment.newspaper(True), """def turn_around():
    for i in range(2):
        turn_left()
for i in range(4):
    move()
    turn_left()
    move()
    turn_right()
    move()
move()
drop_beeper()
turn_around()
move()
for i in range(4):
    move()
    turn_left()
    move()
    turn_right()
    move()
turn_off()
""")
newspaper_fixed.concepts = ["IA1","IB2a"]
newspaper_fixed.difficulty = 1

def newspaper_variable():
    #environment(newspaper.wld)
    # IA1, IB1a, IB1b, IB3, IIA2, IIIA1, IIIA2
    return (environment.newspaper(), """def turn_around():
    for i in range(2):
        turn_left()
pos = 1
while True:
    while front_is_clear():
        move()
        pos += 1
    if pos == 10:
        break
    turn_left()
    while not right_is_clear():
        move()
    turn_right()
drop_beeper()
turn_around()
while True:
    while not left_is_clear() and pos != 1:
        move()
        pos -= 1
    if pos == 1:
        break
    turn_left()
    while front_is_clear():
        move()
    turn_right()
turn_off()
""")
newspaper_variable.concepts = ["IA1","IB1a","IB1b","IB3","IIA2","IIIA1","IIIA2"]
newspaper_variable.difficulty = 9

def hurdles():
    #environment(hurdles?.wld)
    # IA1, IB1a, IB1b, IB3, IIIA2
    return (environment.hurdles(), """def turn_around():
    for i in range(2):
        turn_left()
def walk_to_wall():
    while front_is_clear() and not on_beeper():
        move()
while True:
    walk_to_wall()
    if on_beeper():
        break
    turn_left()
    while not right_is_clear():
        move()
    turn_right()
    move()
    turn_right()
    walk_to_wall()
    turn_left()
turn_off()
""")
hurdles.concepts = ["IA1","IB1a","IB1b","IB3","IIIA2"]
hurdles.difficulty = 4

def harvest():
    #environment(harvest[13].wld)
    # IA1, IA2, IB2a, IB3
    return (environment.harvest(), """def turn_around():
    for i in range(2):
        turn_left()
move()
for i in range(6):
    for i in range(5):
        if on_beeper():
            grab_beeper()
        move()
    if on_beeper():
        grab_beeper()
    if front_is_clear():
        turn_right()
        move()
        turn_right()
    else:
        turn_left()
        move()
        turn_left()
turn_off()
""")
harvest.concepts = ["IA1","IA2","IB2a","IB3"]
harvest.difficulty = 3

def harvest2():
    #environment(harvest2.wld)
    # IB2a, IB3
    size = random.randint(0,1) * 2 + 4
    return (environment.harvest2(size), """def turn_around():
    for i in range(2):
        turn_left()
def move_diagonal():
    turn_right()
    move()
    turn_left()
    move()
def harvest_row():
    for i in range(""" + str(size-1) + """):
        grab_beeper()
        move_diagonal()
    grab_beeper()
def harvest_two_rows():
    harvest_row()
    move()
    turn_left()
    move()
    turn_left()
    harvest_row()
for i in range(""" + str(size-1) + """):
    move()
turn_left()
move()
for i in range(""" + str((size-2) / 2) + """):
    harvest_two_rows()
    turn_right()
    move()
    turn_right()
    move()
harvest_two_rows()
turn_off()
""")
harvest2.concepts = ["IB2a","IB3"]
harvest2.difficulty = 4

def harvest3():
    #environment(harvest4.wld)
    # IA1, IA2, IA3, IB2a, IB3, IIIA2
    return (environment.harvest(True), """def turn_around():
    for i in range(2):
        turn_left()
def garden_spot():
    if not on_beeper():
        drop_beeper()
    else:
        grab_beeper()
        if not on_beeper():
            drop_beeper()
def garden_row():
    for i in range(5):
        garden_spot()
        move()
    garden_spot()
def move_to_next_row():
    if not front_is_clear():
        turn_left()
        move()
        turn_left()
    else:
        turn_right()
        move()
        turn_right()
move()
for i in range(5):
    garden_row()
    move_to_next_row()
garden_row()
move()
turn_left()
for i in range(5):
    move()
turn_left()
turn_off()
""")
harvest3.concepts = ["IA1","IA2","IA3","IB2a","IB3","IIIA2"]
harvest3.difficulty = 7

def maze():
    #environment(maze1.wld)
    # IA2, IB1a, IIIA2
    return (environment.maze(), """def turn_around():
    for i in range(2):
        turn_left()
def traverse_wall():
    while front_is_clear() and not left_is_clear():
        move()
turn_left()
while not on_beeper():
    traverse_wall()
    if left_is_clear() and not on_beeper():
        turn_left()
        move()
    elif not right_is_clear():
        turn_around()
    else:
        turn_right()
turn_off()
""")
maze.concepts = ["IA2","IB1a","IIIA2"]
maze.difficulty = 5

def rain():
    #environment(rain?.wld)
    # IA1, IA2, IA3, IB1a, IIIA2
    return (environment.rain(), """def turn_around():
    for i in range(2):
        turn_left()
def traverse_wall():
    while front_is_clear() and not left_is_clear():
        move()
move()
turn_left()
while not on_beeper():
    if left_is_clear():
        drop_beeper()
        if front_is_clear():
            move()
            if left_is_clear():
                turn_around()
                move()
                grab_beeper()
                turn_right()
                move()
        else:
            turn_right()
    elif not right_is_clear():
        turn_around()
    else:
        turn_right()
    traverse_wall()
grab_beeper()
turn_left()
turn_off()
""")
rain.concepts = ["IA1","IA2","IA3","IB1a","IIIA2"]
rain.difficulty = 7

def trash():
    #environment(trash?.wld)
    # IB1a, IB3
    return (environment.trash(), """def turn_around():
    for i in range(2):
        turn_left()
while front_is_clear():
    move()
    while on_beeper():
        grab_beeper()
turn_around()
while front_is_clear():
    move()
turn_right()
move()
while carries_beepers():
    drop_beeper()
turn_around()
move()
turn_left()
turn_off()
""")
trash.concepts = ["IB1a","IB3"]
trash.difficulty = 2

def rectangle():
    #environment(default+beepers)
    # IB2a, IC, IIB1
    length = random.randint(3,5) if not writeMode else 3
    width = random.randint(3,5) if not writeMode else 4
    return (environment.default(), """def turn_around():
    for i in range(2):
        turn_left()
def line(size):
    for i in range(size):
        drop_beeper()
        move()
def rectangle(width,length):
    size=[width,length]
    move()
    turn_left()
    move()
    turn_right()
    for i in range(4):
        line(size[i%2]-1)
        turn_left()
    turn_around()
    move()
    turn_left()
    move()
    turn_left()
def square(size):
    rectangle(size,size)
rectangle(""" + str(width) + "," + str(length) + """)
turn_off()
""")
rectangle.concepts = ["IB2a","IC","IIB1"]
rectangle.difficulty = 2

def triangle():
    #environment(default+beepers)
    # IB2a, IC, IIB1
    size = random.randint(3,5) if not writeMode else 4
    return (environment.default(), """def turn_around():
    for i in range(2):
        turn_left()
def line(size):
    for i in range(size):
        drop_beeper()
        move()
def diagonal_line(size):
    for i in range(size):
        drop_beeper()
        move()
        turn_left()
        move()
        turn_right()
def triangle(size):
    move()
    turn_left()
    move()
    turn_right()
    line(size-1)
    turn_left()
    diagonal_line(size-1)
    turn_around()
    line(size-1)
    turn_right()
    move()
    turn_left()
    move()
    turn_left()
triangle(""" + str(size) + """)
turn_off()
""")
triangle.concepts = ["IB2a","IC","IIB1"]
triangle.difficulty = 1

def filled_triangle():
    #environment(default+beepers)
    # IA1, IA2, IB2a, IB2c, IC, IIB1, IIIA1, IIIB1, IIIB2, IIIB3
    size = random.randint(2,5) if not writeMode else 4
    return (environment.default(), """def turn_around():
    for i in range(2):
        turn_left()
def line(size):
    for i in range(size):
        move()
        drop_beeper()
def filled_triangle(size):
    for i in range(size+1):
        move()
    for i in range(size,0,-1):
        if (size-i)%2 == 0:
            turn_left()
            move()
            turn_left()
        else:
            move()
            turn_right()
            move()
            turn_right()
        line(i)
    if size%2 == 0:
        turn_around()
    move()
    turn_left()
    for i in range(size):
        move()
    turn_left()
filled_triangle(""" + str(size) + """)
turn_off()
""")
filled_triangle.concepts = ["IA1","IA2","IB2a","IB2c","IC","IIB1","IIIA1","IIIB1","IIIB2","IIIB3"]
filled_triangle.difficulty = 8

def perimeter():
    #environment(amazing?.wld)
    # IA2, IB1a, IIA1, IIA2, IIIA2
    return (environment.perimeter(), """def turn_around():
    for i in range(2):
        turn_left()
def traverse_wall():
    i=0
    while front_is_clear() and not left_is_clear():
        move()
        i+=1
    return i
drop_beeper()
p=1
if left_is_clear():
    turn_left()
    move()
elif front_is_clear():
    move()
else:
    turn_left()
    p=4
while not on_beeper():
    p+=traverse_wall()
    if left_is_clear():
        turn_left()
        move()
    elif not right_is_clear():
        turn_around()
        p+=2
    else:
        turn_right()
        p+=1
grab_beeper()
while not facing_north():
    turn_left()
    p+=1
turn_right()
print "The perimeter is", p
turn_off()
""")
perimeter.concepts = ["IA2","IB1a","IIA1","IIA2","IIIA2"]
perimeter.difficulty = 10

def calendar():
    #environment(corner3_5+beepers)
    # IA2, IB1a, IB2a, IB2c, IB3, IC, IIA1, IIA2, IIB1, IIIA1, IIIB1, IIIB2, IIIB3
    return (environment.default(xpos=3, ypos=5), """def turn_around():
    for i in range(2):
        turn_left()
def week(first,days,dir=1):
    if dir == -1:
        start = first+days-1
        end = first-1
    else:
        start = first
        end = first+days
    for i in range(start,end,dir):
        for j in range(i):
            drop_beeper()
        move()
def calendar(first,days):
    turn_left()
    for i in range(first):
        move()
    week(1,7-first)
    start = 8-first
    dir=0
    while start <= days:
        if dir == 0:
            for i in range(2):
                turn_right()
                move()
            for i in range(start+6-days):
                move()
        else:
            for i in range(2):
                turn_left()
                move()
        week(start,min(days-start+1,7),dir*2-1)
        start += 7
        dir = (dir+1)%2
calendar(4,30)
turn_off()
""")
calendar.concepts = ["IA2","IB1a","IB2a","IB2c","IB3","IC","IIA1","IIA2","IIB1","IIIA1","IIIB1","IIIB2","IIIB3"]
calendar.difficulty = 10

def pattern():
    #environment(default+beepers)
    # IA2, IB1a, IB2a, IB2c, IB3, IC, IIB1, IIIA1, IIIA2, IIIB1
    code = ("""for i in range(4):
    for j in range(5):
        if i+1 == j or j+i == 4:
            drop_beepers(1)
        else:
            drop_beepers(2)
    crlf()""", """for g in range(3):
    for h in range(3):
        if g == h+1 or g+h == 2:
            drop_beepers(1)
        else:
            drop_beepers(2)
    crlf()""")
    return (environment.default(), """def turn_around():
    for i in range(2):
        turn_left()
def crlf():
    turn_left()
    move()
    turn_left()
    while front_is_clear():
        move()
    turn_around()
    move()
def drop_beepers(num):
    for i in range(num):
        drop_beeper()
    move()
move()
""" + code[random.randint(0,1)] + """
turn_off()
""")
pattern.concepts = ["IA2","IB1a","IB2a","IB2c","IB3","IC","IIB1","IIIA1","IIIA2","IIIB1"]
pattern.difficulty = 3

def octagon():
    #environment(corner3_5+beepers)
    # IB2a, IB3, IC, IIB1
    return (environment.default(xpos=7, ypos=2), """def turn_around():
    for i in range(2):
        turn_left()
def line(size):
    for i in range(size):
        drop_beeper()
        move()
def diagonal_line(size):
    for i in range(size):
        drop_beeper()
        move()
        turn_left()
        move()
        turn_right()
def octagon(size):
    for i in range(4):
        diagonal_line(size)
        turn_left()
        line(size)
octagon(2)
turn_off()
""")
octagon.concepts = ["IB2a","IB3","IC","IIB1"]
octagon.difficulty = 2

def pads():
    #environment(fairy_tale+robot2,2E+beeper7,2)
    # IA2, IB1a, IB2a, IB2b, IB3, IIA1, IIA2, IIA3, IIIA1, IIIA2
    return (environment.pads(), """def turn_around():
    for i in range(2):
        turn_left()
def traverse_wall():
    i=0
    while front_is_clear() and not right_is_clear() and not on_beeper():
        move()
        i+=1
    return i
path=[]
p=0
while front_is_clear():
    move()
    p+=1
turn_left()
path.append((p,'L'))
p=traverse_wall()
while not on_beeper():
    if right_is_clear():
        turn_right()
        path.append((p,'R'))
        move()
        p=1
    elif not left_is_clear():
        turn_around()
        path.append((p,'A'))
        p=0
    else:
        turn_left()
        path.append((p,'L'))
        p=0
    p+=traverse_wall()
path.append((p,'A'))
path.reverse()
grab_beeper()
for steps,dir in path:
    if dir == 'L':
        turn_right()
    elif dir == 'R':
        turn_left()
    else:
        turn_around()
    for i in range(steps):
        move()
turn_around()
drop_beeper()
move()
turn_left()
for i in range(2):
    move()
turn_right()
turn_off()
""")
pads.concepts = ["IA2","IB1a","IB2a","IB2b","IB3","IIA1","IIA2","IIA3","IIIA1","IIIA2"]
pads.difficulty = 10

def spaced_beepers():
    #environment(default+beepers)
    # IA1, IB2a, IB2c, IB3, IIIA1, IIIB1
    code = ("""for i in range(10):
    if i%3 == 0:
        drop_beeper()
    move()
turn_off()
""", """for i in range(11):
    if i%2 == 0:
        for j in range(i/2 + 1):
            drop_beeper()
    move()
turn_off()
""")
    return (environment.default(12,12), code[random.randint(0,1)])
spaced_beepers.concepts = ["IA1","IB2a","IB2c","IB3","IIIA1","IIIB1"]
spaced_beepers.difficulty = 1

def planter():
    #environment(plus_sign_in_middle)
    # IA2, IB1a, IIIA2
    corners = random.randint(0,2) if not writeMode else 0
    return (environment.planter(), """def turn_around():
    for i in range(2):
        turn_left()
def move_diagonal():
    move()
    turn_left()
    move()
    turn_right()
def traverse_wall():
    while front_is_clear() and not left_is_clear():
        move()
while front_is_clear() and left_is_clear():
    move_diagonal()
while front_is_clear():
    move()
drop_beeper()
turn_right()
move()
traverse_wall()
while not on_beeper():
""" + ("""    drop_beeper()
""" if corners == 0 else "") +
"""    if left_is_clear():
""" + ("""        drop_beeper()
""" if corners == 1 else "") +
"""        turn_left()
        move()
    else:
""" + ("""        drop_beeper()
""" if corners == 2 else "") +
"""        turn_right()
    traverse_wall()
""" + ("""grab_beeper()
""" if corners == 1 else "") +
"""turn_around()
while front_is_clear() and left_is_clear():
    move_diagonal()
for i in range(2):
    while front_is_clear():
        move()
    turn_left()
turn_off()
""")
planter.concepts = ["IA2","IB1a","IIIA2"]
planter.difficulty = 6

def measurement_dist():
    #environment(default) vary dir?
    # IB1a, IB2a, IC, IIA2, IIB2
    return (environment.default(0,0,0,0), """def turn_around():
    for i in range(2):
        turn_left()
d=0
while front_is_clear():
    move()
    d+=1
turn_around()
for i in range(d):
    move()
turn_around()
print "The distance is", d
turn_off()
""")
measurement_dist.concepts = ["IB1a","IB2a","IC","IIA2","IIB2"]
measurement_dist.difficulty = 2

def measurement_area():
    #environment(corner*_*) vary dir?
    # IB1a, IB2a, IC, IIA2, IIB2
    return (environment.default(0,0,0,0), """def turn_around():
    for i in range(2):
        turn_left()
def dist_to_wall():
    d=0
    while front_is_clear():
        move()
        d+=1
    turn_around()
    for i in range(d):
        move()
    turn_around()
    return d
a=dist_to_wall()
turn_around()
a+=dist_to_wall()
turn_left()
b=dist_to_wall()
turn_around()
b+=dist_to_wall()
turn_right()
print "The area is", (a+1)*(b+1)
turn_off()
""")
measurement_area.concepts = ["IB1a","IB2a","IC","IIA2","IIB2"]
measurement_area.difficulty = 3

def stairs():
    #environment(1x1_stairs_w/beepers_on_top_in_front_of_robot)
    # IB1a
    return (environment.stairs(), """def turn_around():
    for i in range(2):
        turn_left()
while not front_is_clear():
    turn_left()
    move()
    turn_right()
    move()
    grab_beeper()
turn_off()
""")
stairs.concepts = ["IB1a"]
stairs.difficulty = 1

def mountain():
    #environment(mountain)
    # IB1a, IIA2, IIIA1, IIIA2
    return (environment.mountain(), """def turn_around():
    for i in range(2):
        turn_left()
while front_is_clear():
    move()
h=0
while not front_is_clear():
    turn_left()
    while not right_is_clear():
        move()
        h += 1
    turn_right()
    move()
drop_beeper()
while h > 0:
    move()
    turn_right()
    while front_is_clear():
        move()
        h -= 1
    turn_left()
turn_off()
""")
mountain.concepts = ["IB1a","IIA2","IIIA1","IIIA2"]
mountain.difficulty = 9

def mover():
    #environment(line_of_beepers_in_front_of_robot)
    # IB1a, IB3, IB2a, IIA2, IIIA2
    return (environment.mover(), """def turn_around():
    for i in range(2):
        turn_left()
while not on_beeper():
    move()
b=0
while on_beeper():
    grab_beeper()
    move()
    b+=1
turn_left()
for i in range(b):
    move()
turn_left()
for i in range(b):
    move()
    drop_beeper()
for i in range(2):
    while front_is_clear():
        move()
    turn_left()
turn_off()
""")
mover.concepts = ["IB1a","IB3","IB2a","IIA2","IIIA2"]
mover.difficulty = 3

def bowling():
    #environment(default+beepers)
    # IA1, IA2, IB2a, IB2c, IC, IIB1, IIIB1
    rows = random.randint(3,4) if not writeMode else 4
    return (environment.default(), """def turn_around():
    for i in range(2):
        turn_left()
def line(size):
    for i in range(size):
        move()
        drop_beeper()
        move()
def bowling_pins(size):
    for i in range(4):
        move()
    for i in range(size):
        move()
        if i%2 == 0:
            turn_left()
            move()
            turn_left()
        else:
            turn_right()
            move()
            turn_right()
        line(i+1)
    if size%2 == 0:
        turn_around()
    while front_is_clear():
        move()
    turn_left()
    for i in range(size):
        move()
    turn_left()
bowling_pins(""" + str(rows) + """)
turn_off()
""")
bowling.concepts = ["IA1","IA2","IB2a","IB2c","IC","IIB1","IIIB1"]
bowling.difficulty = 8

def spiral():
    #environment(corner5_5+facing_east)
    # IB1a, IB3, IIA1, IIA2, IIIA1, IIIA2
    return (environment.spiral(0), """def turn_around():
    for i in range(2):
        turn_left()
i=1
j=1
while j == i:
    j=1
    while j <= i and front_is_clear():
        drop_beeper()
        move()
        j+=1
    turn_left()
    i+=1
turn_off()
""")
spiral.concepts = ["IB1a","IB3","IIA1","IIA2","IIIA1","IIIA2"]
spiral.difficulty = 6

problems = (stairs, newspaper_fixed, spaced_beepers, triangle, octagon, rectangle, trash, measurement_dist, measurement_area, mover, harvest, pattern, hurdles, harvest2, maze, spiral, planter, harvest3, rain, bowling, filled_triangle, mountain, newspaper_variable, calendar, perimeter, pads)

tracing = (newspaper_fixed, spaced_beepers, triangle, octagon, rectangle, trash, mover, pattern, hurdles, harvest2, maze, spiral, planter, rain, bowling, filled_triangle, mountain, newspaper_variable, perimeter, pads)

writing = (stairs, newspaper_fixed, triangle, octagon, rectangle, trash, measurement_dist, measurement_area, mover, harvest, hurdles, harvest2, maze, spiral, planter, harvest3, rain, bowling, filled_triangle, mountain, newspaper_variable, calendar, perimeter, pads)

