import random

def default(width=10,height=10,xpos=1,ypos=1,dir='E',beepers=600):
    if width == 0:
        width = random.randint(4,12)
    if height == 0:
        height = random.randint(4,12)
    if xpos == 0:
        xpos = random.randint(1,width)
    if ypos == 0:
        ypos = random.randint(1,height)
    env = {}
    env['avenues'] = width
    env['streets'] = height
    env['robot'] = (xpos,ypos,dir,beepers)
    env['walls'] = []
    env['beepers'] = {}
    return env

def stairs(height=0):
    if height == 0:
        height = random.randint(1,8)
    env = default(beepers=0)
    for i in range(height*2):
        env['walls'].append((i+2,i+1))
    backX = (height+1)*2
    for i in range(height*2 - 1, 0, -2):
        env['walls'].append((backX,i))
    for i in range(2,2+height):
        env['beepers'][(i,i)] = 1
    return env

def trash(height=1):
    if height == 0:
        height = random.randint(1,4)
    env = default(beepers=0)
    for i in range(3,20,2):
        env['walls'].append((i,height*2))
    env['walls'].append((1,(height+1) * 2))
    env['walls'].append((2,height*2 + 1))
    while not env['beepers']: # make sure there's some trash
        for i in range(1,height+1):
            for j in range(2,11):
                if random.random() < 1.0/(height+2):
                    m = 10
                    b = random.randint(1,m)
                    if b > m/2 and random.random() < 1.0/2:
                        b = m - b + 1
                    env['beepers'][(j,i)] = b
    return env

# measurement default(0,0,0,0) vary dir?

def mover(beepers=0,first=0):
    if beepers == 0:
        beepers = random.randint(2,6)
    if first == 0:
        first = random.randint(2,10-beepers)
    env = default(beepers=0)
    for i in range(first,first+beepers):
        env['beepers'][(i,1)] = 1
    return env

def harvest(weeds=False,holes=True):
    env = default(width=7, height=7)
    for i in range(2,8):
        for j in range(1,7):
            r = random.random()
            if not holes or r > 1.0/6:
                env['beepers'][(i,j)] = 1
                if weeds and r < 2.0/6:
                    env['beepers'][(i,j)] = 2
    return env

# True is variable, False is fixed
def hurdles(spacing=True,height=True,finish=True):
    env = default(beepers=0)
    hurdles = []
    if spacing:
        for i in range(1,10):
            if random.random() > 1.0/3:
                hurdles.append(i*2)
    else:
        hurdles = range(4,20,4)
    for i in hurdles:
        if height:
            h = random.randint(0,3) % 3 + 1
        else:
            h = 1
        for j in range(1, h*2, 2):
            env['walls'].append((i,j))
    if finish:
        env['beepers'][(random.randint(6,10),1)] = 1
    else:
        env['beepers'][(10,1)] = 1
    return env

def harvest2(size=6):
    env = default(width=size*2, height=size*2, beepers=0)
    for i in range(1,size+1):
        j = size+2-i
        for k in range(size):
            env['beepers'][(i+k,j+k)] = 1
    return env

# DFS
def maze(size=5):
    if size == 0:
        size = random.randint(4,7)
    def neighbors(cell):
        x,y = cell
        cells = []
        n = size
        if x > 1: cells.append((x-1,y))
        if y > 1: cells.append((x,y-1))
        if x < n: cells.append((x+1,y))
        if y < n: cells.append((x,y+1))
        return cells
    walls = set()
    visited = set()
    for i in range(1, size*2, 2):
        for j in range(2, size*2 + 1, 2):
            walls.add((i,j))
            walls.add((j,i))
    walls.remove((size*2,size*2 - 3))
    def build(cur):
        visited.add(cur)
        nei = neighbors(cur)
        yet = []
        for cell in nei:
            if cell not in visited:
                yet.append(cell)
        if len(yet) > 0:
            i = random.randint(0,len(yet)-1)
            nex = yet.pop(i)
            yet.insert(0, nex)
            for nex in yet:
                if nex not in visited:
                    walls.remove((cur[0]+nex[0]-1, cur[1]+nex[1]-1))
                    build(nex)
    build((size, size-1))
    env = default(beepers=0)
    env['walls'] = list(walls)
    env['beepers'][(size+1,size-1)] = 1
    return env

# randomized Prim
def maze2(size=5):
    if size == 0:
        size = random.randint(4,7)
    def neighbors(cell):
        x,y = cell
        cells = []
        n = size
        if x > 1: cells.append((x-1,y))
        if y > 1: cells.append((x,y-1))
        if x < n: cells.append((x+1,y))
        if y < n: cells.append((x,y+1))
        return cells
    walls = set()
    visited = set()
    for i in range(1, size*2, 2):
        for j in range(2, size*2 + 1, 2):
            walls.add((i,j))
            walls.add((j,i))
    walls.remove((size*2,size*2 - 3))
    cells = set()
    cur=(size, size-1)
    visited.add(cur)
    for cell in neighbors(cur):
        cells.add(cell)
    while len(cells) > 0:
        i = random.randint(0, len(cells)-1)
        nex = list(cells)[i]
        cells.remove(nex)
        if nex not in visited:
            oth = neighbors(nex)
            rem = []
            for cell in oth:
                if cell in visited:
                    rem.append(cell)
            i = random.randint(0, len(rem)-1)
            nei = rem[i]
            walls.remove((nex[0]+nei[0]-1, nex[1]+nei[1]-1))
            visited.add(nex)
            for cell in neighbors(nex):
                if cell not in visited: cells.add(cell)
    env = default(beepers=0)
    env['walls'] = list(walls)
    env['beepers'][(size+1,size-1)] = 1
    return env

# recursive division
def maze3(size=5):
    if size == 0:
        size = random.randint(4,7)
    walls = set()
    for i in range(1, size*2, 2):
        walls.add((i,size*2))
        walls.add((size*2,i))
    walls.remove((size*2,size*2 - 3))
    def div(lox,hix,loy,hiy):
        if lox == hix or loy == hiy:
            return
        a = random.randint(lox+1,hix)
        b = random.randint(loy+1,hiy)
        for i in range(loy*2+1, (hiy+1)*2, 2):
            walls.add((a*2,i))
        for i in range(lox*2+1, (hix+1)*2, 2):
            walls.add((i,b*2))
        out = []
        out.append((random.randint(lox,a-1)*2 + 1,b*2))
        out.append((random.randint(a,hix)*2 + 1,b*2))
        out.append((a*2,random.randint(loy,b-1)*2 + 1))
        out.append((a*2,random.randint(b,hiy)*2 + 1))
        out.pop(random.randint(0,3))
        for wall in out:
            walls.remove(wall)
        div(lox,a-1,b,hiy)
        div(lox,a-1,loy,b-1)
        div(a,hix,b,hiy)
        div(a,hix,loy,b-1)
    div(0,size-1,0,size-1)
    env = default(beepers=0)
    env['walls'] = list(walls)
    env['beepers'][(size+1,size-1)] = 1
    return env    

def spiral(size=10):
    if size == 0:
        size = random.randint(6,12)
    c = (size+1) / 2
    return default(width=size, height=size, xpos=c, ypos=c)

# TODO: vary shape of structure
def planter():
    env = default()
    for i in range(5,16,2):
        env['walls'].append((i,10))
        env['walls'].append((10,i))
    return env

def rain(rectangle=False):
    env = default(12, 12, 2, 6)
    if rectangle:
        top = 8
        bottom = 3
        end = 16
    else:
        top = random.randint(8,11)
        bottom = random.randint(1,3)
        end = 22
    for y in 7,9,13,15:
        env['walls'].append((4, y))
    window = False
    env['walls'].append((5, 6))
    env['walls'].append((5, 16))
    env['walls'].append((15, 6))
    env['walls'].append((15, 16))
    for y in 6, 16:
        for x in range(7, 14, 2):
            if window or random.random() < .5:
                env['walls'].append((x, y))
                window = False
            else:
                window = True
        window = False
    if top > 8:
        env['walls'].append((16, 17))
        if top == 10:
            env['walls'].append((16, 19))
        elif top == 11:
            if random.random() < .5:
                env['walls'].append((16, 19))
            env['walls'].append((16, 21))
        env['walls'].append((17, top*2))
        if random.random() < .5:
            env['walls'].append((19, top*2))
        env['walls'].append((21, top*2))
    elif not rectangle:
        for x in 17, 19:
            if window or random.random() < .5:
                env['walls'].append((x, 16))
                window = False
            else:
                window = True
        window = False
        env['walls'].append((21, 16))
    if bottom < 3:
        env['walls'].append((16, 5))
        if bottom == 1:
            env['walls'].append((16, 3))
        env['walls'].append((17, bottom*2))
        if random.random() < .5:
            env['walls'].append((19, bottom*2))
        env['walls'].append((21, bottom*2))
    elif not rectangle:
        for x in 17, 19:
            if window or random.random() < .5:
                env['walls'].append((x, 6))
                window = False
            else:
                window = True
        window = False
        env['walls'].append((21, 6))
    env['walls'].append((end, top*2 - 1))
    for y in range(top*2 - 3, bottom*2 + 2, -2):
        if window or random.random() < .5:
            env['walls'].append((end, y))
            window = False
        else:
            window = True
    env['walls'].append((end, bottom*2 + 1))
    return env

def mountain():
    env = default()
    height = random.randint(3, 8)
    steps = random.randint(2, min(height,5))
    stepsdown = random.randint(2, 7-steps)
    start = random.randint(2, 9-(steps+stepsdown))
    def subdivide(h, steps):
        inc = []
        c = 0
        for i in range(steps-1, 0, -1):
            n = random.randint(1, h-i-c)
            inc.append(n)
            c += n
        inc.append(height - c)
        return inc
    up = subdivide(height, steps)
    down = subdivide(height, stepsdown)
    x = start*2
    y = 1
    for c in up:
        for i in range(c):
            env['walls'].append((x, y))
            y += 2
        env['walls'].append((x+1, y-1))
        x += 2
    y -= 2
    for c in down:
        for i in range(c):
            env['walls'].append((x, y))
            y -= 2
        if y > 0: env['walls'].append((x+1, y+1))
        x += 2
    return env

def newspaper(fixed=False):
    env = default()
    x = 5
    y = 0
    while x < 20:
        y += 2
        env['walls'].append((x-1, y-1))
        for i in range(x, (x+3) if fixed else min(random.randint(x+1, x+5), 20), 2):
            x = i
            env['walls'].append((x, y))
        x += 2
    return env

def perimeter(amazing=0):
    if amazing == 0:
        amazing = random.randint(1,4)
    if amazing == 1:
        return default(5,5)
    if amazing == 2:
        env = default(7,7)
        for i in range(7, 14, 2):
            env['walls'].append((6, i))
            env['walls'].append((i, 6))
        return env
    if amazing == 3:
        env = default(7,7)
        env['walls'].append((2, 1))
        env['walls'].append((3, 2))
        env['walls'].append((5, 2))
        for i in range(3, 14, 2):
            env['walls'].append((6, i))
        return env
    env = default(7,7)
    env['walls'].append((4, 1))
    env['walls'].append((3, 2))
    env['walls'].append((2, 3))
    env['walls'].append((3, 4))
    env['walls'].append((5, 4))
    for i in range(5, 14, 2):
        env['walls'].append((6, i))
    return env

def pads(lockers=0,roy=0,width=0):
    if lockers == 0:
        lockers = random.randint(4,7)
    if roy == 0:
        roy = random.randint(1, lockers-3)
    if width == 0:
        width = random.randint(5,7)
    env = default(8,8,1,roy,beepers=0)
    for i in range(2, lockers*2 + 1, 2):
        env['walls'].append((1, i))
    x = 3
    if width == 7:
        env['walls'].append((x, lockers*2))
        x += 2
    for i in range(5):
        env['walls'].append((x+i, lockers*2 - i))
    x += 6
    y = lockers*2 - 2
    env['walls'].append((x, y))
    if width > 5:
        x += 2
        env['walls'].append((x, y))
    x += 1
    y -= 1
    for i in range(y, 0, -2):
        env['walls'].append((x, i))
    env['beepers'][(x/2 + 1, random.randint(1, lockers-2))] = 1
    env['beepers'][(1, roy+2)] = 1
    return env

def printenv(env):
    out = file('/tmp/foo.wld','w')
    for key in env:
        out.write(key)
        out.write(' = ')
        out.write(str(env[key]))
        out.write('\n')
    out.close()
