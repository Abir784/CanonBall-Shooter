from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random


height = 600
width = 800



g = 9.8 
v0 = 85
angle = 45 
bullets = []

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)



def draw_projectile(x, y):
    glColor3f(0.0, 1.0, 0.0)
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def zone_check(x0,y0,x1,y1):
    x_t0 = x0
    x_t1 = x1
    y_t0 = y0
    y_t1 = y1
    dy = y1 - y0
    dx = 1
    if x1 != x0:
        dx = x1 - x0
    slope = dy/dx
    line_pixels = []
    zone1 = zone2 = zone3 = False
    if slope>1:
        x_t0 = y0
        y_t0 = x0
        x_t1 = y1
        y_t1 = x1
        zone1 =True
    elif slope < -1:
        x_t0 = -y0
        x_t1 = -y1
        y_t0 = x0
        y_t1 = x1
        zone2 = True
    elif -1 <= slope < 0:
        x_t0 = x0
        x_t1 = x1
        y_t0 = -y0
        y_t1 = -y1
        zone3 = True
    return [x_t0,y_t0,x_t1,y_t1,zone1,zone2,zone3]
    
def mpl(x0, y0, x1, y1):
    x_t0 ,y_t0, x_t1, y_t1 , zone1, zone2, zone3 = zone_check(x0,y0,x1,y1)


    dy = y_t1 - y_t0
    dx = 1
    if x_t0 != x_t1:
        dx = x_t1 - x_t0
    d = (2 * dy ) - dx                         
    x, y = x_t0, y_t0


    while (x <= x_t1):
        if zone1:
            glVertex2f(y,x)
        elif zone2:

            glVertex2f(y,-x)
        elif zone3:

            glVertex2f(x,-y)
        else:
            glVertex2f(x,y)
        
        if d >= 0:
            d += (2*dy)-(2*dx)
            x+=1
            y+=1
        else:
            d += 2*dy
            x+=1

def octant_points(cx, cy, x, y):
    glVertex2f(cx + x, cy + y)
    glVertex2f(cx - x, cy + y)
    glVertex2f(cx + x, cy - y)
    glVertex2f(cx - x, cy - y)
    glVertex2f(cx + y, cy + x)
    glVertex2f(cx - y, cy + x)
    glVertex2f(cx + y, cy - x)
    glVertex2f(cx - y, cy - x)

def mpc(cx, cy, r):
    d = 1 - r
    x = 0
    y = r

    while x <= y:
        octant_points(cx,cy,x,y)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1


def collision_check():
    global circle_info, paused, score,missed,firing 

    for circle in circle_info:
        distance = ((circle[0] - fireset[0])**2 + (circle[1] - fireset[1])**2)**0.5

        if distance <= fireset[2] + circle[2]:
            fireset[1] = 215
            circle_info.remove(circle)
            score += 1
            firing = False

            print("Score: ",score)
        
        if (290+rocket_move<= circle[0]<= 430+rocket_move) and (circle[1]+circle[2] <= 210):
            print("game over hit by asteroid")
            print("Score : ",score)
            os._exit(0)

def draw_allien():
    r = 10
    mpc(30,80,r)
    mpl(20,80,30,40)
    mpl(30,40,40,80)
    mpl(35,90,45,95) #antena



    

def keyboardListener(key, x, y):
    global angle, bullets

    if key == b' ': 
        vx = v0 * math.cos(math.radians(angle))
        vy = v0 * math.sin(math.radians(angle))
        bullets.append({'x':750,'y':50,"vx":vx,"vy":vy,"t":0})
    elif key == b'w':  
        angle = min(angle + 5, 90) 
    elif key == b's':  
        angle = max(angle - 5, 0)
    glutPostRedisplay()

def mouseListener(button, state, x, y):	
    global paused,rocket_move,circle_info,fireset
    y = abs(y - height)
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
                if height-50 <= y <= height:
                    if 0<= x <= 50:
                        fireset[1] = 215
                        rocket_move = 0
                        circle_info = []
                        score = 0
                    elif 350 <= x <= 370:
                        if paused:
                            paused = False
                            print("resume")
                        else:
                            paused = True
                            print("Paused")
                    elif width-50 <= x <= width:
                        print("exited")
                        os._exit(0)
                    
     

    glutPostRedisplay()

def timer(t):
    glutPostRedisplay()
    glutTimerFunc(20, timer, 0)

def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def display():
    global bullets
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glClearColor(1, 1, 1, 1) 
    glClearColor(0.0, 0.0, 0.0, 0.0)
    
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    iterate()

    # my work
    # navigation_bar()
    new_bullets = []
    for bullet in bullets:
        t = bullet['t']
        px = bullet['x'] - bullet['vx'] * t
        py = bullet['y'] + bullet['vy'] * t - 0.5 * g * t ** 2

        if px >= -1 and py >=-1 :
            draw_projectile(px, py)
            bullet['t'] += 0.05
            new_bullets.append(bullet)

    bullets = new_bullets
    glPointSize(1)
    glBegin(GL_POINTS)
    glColor(1,0,0)
    draw_allien()
    glEnd()
    glutSwapBuffers()  



glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(width, height)  
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Lab Assignment 2")
glutDisplayFunc(display)
# glutIdleFunc(animate)
# glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)
glutKeyboardFunc(keyboardListener)
glutTimerFunc(10, timer, 0)
glutMainLoop()

