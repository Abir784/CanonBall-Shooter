from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


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


def keyboardListener(key, x, y):
    global firing,rocket_move,fireset
    if paused == False:
        if key== b'a':		
            if rocket_move > -360+80:
                rocket_move -=20
                fireset[0] -= 20
        if key== b'd':		
            if rocket_move<360-80:
                rocket_move +=20
                fireset[0]+=20
        if key==b' ':
            firing = True
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



def iterate():
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glClearColor(1, 1, 1, 1) 
    glClearColor(0.0, 0.0, 0.0, 0.0)
    
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    iterate()

    # my work
    navigation_bar()
    rocket()
    glBegin(GL_POINTS)
    glColor(1,0,1)
    for circle in circle_info:
        mpc(circle[0], circle[1], circle[2])

    glColor(1,1,0)
    mpc(fireset[0],fireset[1],fireset[2])
    glEnd()
    glutSwapBuffers()  



# glutInit()
# glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
# glutInitWindowSize(width, height)  
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow(b"Lab Assignment 2")
# glutDisplayFunc(display)
# glutIdleFunc(animate)
# glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
# glutMainLoop()

