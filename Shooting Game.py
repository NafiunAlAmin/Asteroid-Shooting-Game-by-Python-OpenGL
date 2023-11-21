from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import math

# Global variables for UFO animation
x_pos = 370
radius_x = 100
object_width = radius_x
target_x_pos = x_pos
radius_y = 25
points = 0

def draw_ufo(center_x, center_y, radius_x, radius_y, num_segments):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(center_x, center_y)

    for i in range(num_segments + 1):
        angle = 2.0 * math.pi * i / num_segments
        x = center_x + radius_x * math.cos(angle)
        y = center_y + radius_y * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw stars
    no_stars = 1000
    for i in range(no_stars):
        x = random.randint(0, 800)
        y = random.randint(0, 800)
        color = (random.uniform(0.4,0.59), 0.0, random.uniform(0.49,0.8))
        stars(x, y, color)

    if points>99:
        glColor3f(1,1,1)

        e(100,400,200,500)
        n(250,400,350,500)
        d(400,400,500,500)
    else:
        #Draw Meteorite
        for j in rocks:
            j.draw()

        for k in attacks:
            k.draw()
        #Draw Ufo
        glColor3f(0.8, 0.8, 0.8)
        draw_ufo(x_pos, 100, radius_x, radius_y, 100)

        glColor3f(0.2, 0.2, 0.2)
        draw_ufo(x_pos, 125, radius_x * 0.6, radius_y * 0.6, 100)


    glColor3f(1,1,1)
    pointcount(points)
    glutSwapBuffers()

def update_values(value):
    global x_pos, target_x_pos
    if points<100:
        diff = target_x_pos - x_pos
        x_pos += diff * (0.5)

        glutPostRedisplay()
        glutTimerFunc(16, update_values, value)

attacks=[] #attack global varaible

class attack:
    def __init__(self, x_pos):
        self.x = x_pos
        self.y = 125
        self.speed = 10
        self.state = True

    def draw(self):
        glColor3f(0.8, 0,0)
        midpointCircle(5,self.x,self.y)

def key_input(key, x, y):
    global target_x_pos
    global attacks

    if key == GLUT_KEY_RIGHT and target_x_pos < 800-130:
        target_x_pos += 50
    elif key == GLUT_KEY_LEFT and target_x_pos > 0+130:
        target_x_pos -= 50
    elif key == GLUT_KEY_UP:
        attacks.append(attack(target_x_pos))

# Global variables for stars and meteorites
rocks = []

class meteorite:
    def __init__(self):
        self.x = random.randint(130, 800-130)
        self.y = 800
        self.size = random.randint(30, 70)
        self.speed = 1.5 #random.uniform(0.5, 1)
        self.color = (random.uniform(0.15,0.25),random.uniform(0.08,0.12), 0.0)
        self.status=True

    def draw(self):
        #meterorites
        glColor3fv(self.color)
        glBegin(GL_POLYGON)
        for i in range(8):
            angle = 2 * math.pi * i / 8
            vertex_x = self.x + self.size * math.cos(angle)
            vertex_y = self.y + self.size * math.sin(angle)
            glVertex2f(vertex_x, vertex_y)
        glEnd()
        #meteorite outline
        glColor3f(0.17, 0.08, 0.02)
        glLineWidth(5.0)
        glBegin(GL_LINE_LOOP)
        for i in range(8):
            angle = 2 * math.pi * i / 8
            vertex_x = self.x + self.size * math.cos(angle)
            vertex_y = self.y + self.size * math.sin(angle)
            glVertex2f(vertex_x, vertex_y)
        glEnd()

def stars(x, y, color):
    glColor3fv(color)
    glPointSize(random.randint(1, 3))
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def update(value):
    global rocks
    global attacks
    global points

    if points<100:
        #meteorite
        new_rocks = []
        for rock in rocks:
            rock.y = rock.y - rock.speed
            if rock.y > 0 and rock.status==True:
                new_rocks.append(rock)
        rocks = new_rocks

        #attack
        new_attacks = []
        for attack in attacks:
            attack.y += attack.speed
            if attack.y < 800 and attack.state==True:
                new_attacks.append(attack)
        attacks = new_attacks

        #damage
        for attack in attacks:
            if attack.state==False:
                continue
            a=0
            b=0
            for rock in rocks:
                if rock.status==False:
                    continue
                a=rock.x-attack.x
                b=rock.y-attack.y
                if math.sqrt((a**2)+(b**2))<rock.size+5+5:
                    rock.status=False
                    attack.state=False
                    if rock.size>=65:
                        points+=15
                    else:
                        points+=10

    glutPostRedisplay()
    glutTimerFunc(1, update, value)

def create_meteorite(value):
    global rocks
    if points<100:
        rocks.append(meteorite())
        glutTimerFunc(random.randint(500, 2000), create_meteorite, value)

#Point Generation
def draw_points(x, y):
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

def findZone(x0, y0, x1, y1):
    dy = y1 - y0
    dx = x1 - x0
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dy > 0:
            return 1
        else:
            return 5


def zeroconvert(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def originalconvert(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, -x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y


def midpointline(x1, y1, x2, y2, z):
    dx = x2 - x1
    dy = y2 - y1
    x = x1
    y = y1
    d = (2 * dy) - dx
    east = 2 * dy
    northeast = 2 * (dy - dx)
    if dx == 0:
        while y <= y2:
            t1, t2 = originalconvert(x, y, z)
            draw_points(t1, t2)
            y += 1
    else:
        while x <= x2:
            t1, t2 = originalconvert(x, y, z)
            draw_points(t1, t2)
            x += 1
            if d > 0:
                d += northeast
                y += 1
            else:
                d += east

def eightSem(x0, y0, x1, y1):
    z = findZone(x0,y0,x1,y1)
    x0_0, y0_0 = zeroconvert(x0, y0, z)
    x1_0, y1_0 = zeroconvert(x1, y1, z)
    midpointline(x0_0, y0_0, x1_0, y1_0, z)

def zero(x1,y1,x2,y2):
    eightSem(x1,y1,x2,y1)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, y2)
    eightSem(x1, y1, x1, y2)

def one(x1,y1,x2,y2):
    eightSem(x2, y1, x2, y2)


def two(x1,y1,x2,y2):
    eightSem(x1,y1,x2,y1)
    eightSem(x1, (y1+y2)//2, x2, (y1+y2)//2)
    eightSem(x1, y2, x2, y2)
    eightSem(x1, y1, x1, (y1+y2)//2)
    eightSem(x2, (y1+y2)//2, x2, y2)

def three(x1,y1,x2,y2):
    eightSem(x1, y1, x2, y1)
    eightSem(x1, y2, x2, y2)
    eightSem(x1, (y1+y2)//2, x2, (y1+y2)//2)
    eightSem(x2, y1, x2, y2)

def four(x1,y1,x2,y2):
    eightSem(x1, (y1+y2)//2, x2, (y1+y2)//2)
    eightSem(x1, y2, x1, (y1+y2)//2)
    eightSem(x2, y1, x2, y2)

def five(x1,y1,x2,y2):
    eightSem(x1,y1,x2,y1)
    eightSem(x1, (y1+y2)//2, x2, (y1+y2)//2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, (y1 + y2) // 2)
    eightSem(x1, (y1 + y2) // 2, x1, y2)

def six(x1,y1,x2,y2):
    eightSem(x1,y1,x2,y1)
    eightSem(x1, (y1+y2)//2, x2, (y1+y2)//2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, (y1+y2)//2)
    eightSem(x1, y1, x1, y2)

def seven(x1,y1,x2,y2):
    eightSem(x1,y2,x2,y2)
    eightSem(x2, y1, x2, y2)

def eight(x1,y1,x2,y2):
    eightSem(x1,y1,x2,y1)
    eightSem(x1, (y1+y2)//2, x2, (y1+y2)//2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, y2)
    eightSem(x1, y1, x1, y2)

def nine(x1,y1,x2,y2):
    eightSem(x1,y1,x2,y1)
    eightSem(x1, (y1+y2)//2, x2, (y1+y2)//2)
    eightSem(x1, y2, x2, y2)
    eightSem(x2, y1, x2, y2)
    eightSem(x1, y2, x1, (y1+y2)//2)

def e(x1,y1,x2,y2):
    eightSem(x1,y1,x1,y2)
    eightSem(x1,y1,x2,y1)
    eightSem(x1,y2,x2,y2)
    eightSem(x1,(y1+y2)/2,x2,(y1+y2)/2)

def n(x1,y1,x2,y2):
    eightSem(x1, y1, x1, y2)
    eightSem((x1+x2)/2, y1+49, (x1+x2)/2, y2-49)
    eightSem(x1, y2, (x1+x2)/2, y2-49)
    eightSem((x1 + x2) / 2, y1+49,x2, y1)
    eightSem(x2, y1, x2, y2)

def d(x1,y1,x2,y2):
    eightSem(x2, y1+20, x2, y2-20)
    eightSem(x1, y1, x2, y1+20)
    eightSem(x1, y2, x2, y2-20)
    eightSem(x1, y1, x1, y2)
def pointcount(p):
    bleep=str(p)
    x1, y1 = 10, 760
    x2, y2 = 20, 790
    for i in bleep:
        if i == '0':
            zero(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == '1':
            one(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == '2':
            two(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == '3':
            three(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == '4':
            four(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        elif i == '5':
            five(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == '6':
            six(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == '7':
            seven(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == '8':
            eight(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)
        if i == '9':
            nine(x1, y1, x2, y2)
            x1, x2 = increase(x1, x2)


def increase(x1, x2):
    a = x2 + 10
    b = x2+10+(x2-x1)
    return a, b
def circlePoints(x,y,x1,y1):
    draw_points(x+x1,y+y1) #0
    draw_points(y+x1, x+y1) #1
    draw_points(-y+x1,x+y1) #2
    draw_points(-x+x1, y+y1) #3
    draw_points(-x+x1, -y+y1) #4
    draw_points(-y+x1,-x+y1) #5
    draw_points(y+x1,-x+y1) #6
    draw_points(x+x1, -y+y1) #7


def midpointCircle(r, a, b):
    d=1-r
    x,y=0,r
    circlePoints(x,y,a,b)
    while y>x:

        if d<0:
            d=d+x*2+3
            x+=1
        else:
            d=d+(x-y)*2+5
            x+=1
            y-=1
        circlePoints(x,y,a,b)
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(0,0)
    glutCreateWindow("UFO Animation and Meteorites")

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 800, 0, 800, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(draw)
    glutSpecialFunc(key_input)
    glutTimerFunc(16, update_values, 0)#chatgpt ask
    glutTimerFunc(0, update, 0)
    glutTimerFunc(0, create_meteorite, 0)
    if points >= 20:
        sys.end()
    glutMainLoop()


if __name__ == "__main__":
    main()