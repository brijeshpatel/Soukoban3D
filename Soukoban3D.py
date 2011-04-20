#!/usr/bin/python
import gutil
import pygame
pygame.init()
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import os
import time
import string
pygame.init()
from pygame.locals import *
SCREEN_SIZE = (640,480)
level=1
targetCount=0
brikTex=0
cube_list=0
redBlock=0
block=0
mapArr = []
currentPosition = [1,3]
moves=0
cameraFrom = [-50,140,-50]
cameraTo = [-40,0,-40]
def draw_string(x, y, z, txt):
    glRasterPos3f(x, y, z)
    for c in txt:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))
        
def loadLevel(i):
    global mapArr,targetCount,moves,currentPosition
    mapArr=[]
    targetCount=0
    moves=0
    f = open('level'+str(i)+'.txt', 'r+')
    line = f.readline()
    j=0
    while(line!=''):
        mapArr.append(line.split(' '))
        j=j+1
        line = f.readline()
    for i in range(len(mapArr)):
        for j in range(len(mapArr[i])):
            if(mapArr[i][j]=="P"):
                currentPosition[0]=i
                currentPosition[1]=j
                mapArr[i][j]="0"
            if(mapArr[i][j]=="T"):
                targetCount=targetCount+1

def loadImage(image):
     textureSurface = pygame.image.load(image)
 
     textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
 
     width = textureSurface.get_width()
     height = textureSurface.get_height()
 
     texture = glGenTextures(1)
     glBindTexture(GL_TEXTURE_2D, texture)
     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
     glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData )
 
     return texture, width, height
 

def drawCube(texlist,i,j,brikTex):
    tx,ty,tz=(-j*10+5,10,-i*10+5)
    glBindTexture(GL_TEXTURE_2D, brikTex)
    glLoadIdentity()
    gluLookAt(cameraFrom[0],cameraFrom[1],cameraFrom[2],cameraTo[0],cameraTo[1],cameraTo[2],0,0,1)
    glTranslatef(tx,ty,tz)
    glCallList(texlist)


def initShapes():
    cube_list = glGenLists(1)
    x, y, z = (5.0,5.0,5.0)
    glNewList(cube_list,GL_COMPILE)
    glBegin(GL_QUADS)
    ## Front Face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, -y,  z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( x, -y,  z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( x,  y,  z)
    glTexCoord2f(0, 1)
    glVertex3f(-x,  y,  z)
    ## Back Face
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-x, -y, -z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-x,  y, -z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f( x, y, -z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f( x, -y, -z)
    ## Top Face
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-x,y, -z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, y,  z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( x,  y,  z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( x,  y, -z)
    ## Bottom Face
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-x, -y, -z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f( x, -y, -z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f( x, -y,  z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-x, -y, z)
    ## Right face
    glTexCoord2f(1.0, 0.0)
    glVertex3f( x, -y, -z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( x,  y, -z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f( x,  y,  z)
    glTexCoord2f(0.0, 0.0)
    glVertex3f( x, -y,  z)
    ## Left Face
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, -y, -z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(-x, -y,  z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(-x,  y,  z)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-x,  y, -z)
    glEnd()
    glEndList()
    floor_list = glGenLists(1)
    x, y, z = (10.0,10.0,10.0)
    glNewList(floor_list,GL_COMPILE)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-x, 0,  -z)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( x, 0,  -z)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( x,  0,  z)
    glTexCoord2f(0, 1)
    glVertex3f(-x,  0,  z)
    glEnd()
    glEndList()
    return cube_list,floor_list
def drawTarget(i,j):
    texture, w, h = loadImage('target.png')
    glBindTexture(GL_TEXTURE_2D, texture)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(cameraFrom[0],cameraFrom[1],cameraFrom[2],cameraTo[0],cameraTo[1],cameraTo[2],0,0,1)
    glTranslatef(-j*10+5,5,-i*10+5)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5, 0,  -5)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 5, 0,  -5)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 5,  0,  5)
    glTexCoord2f(0, 1)
    glVertex3f(-5,  0,  5)
    glEnd()
    glPopMatrix()
    
def drawPerson():
    i=currentPosition[0]
    j=currentPosition[1]
    texture, w, h = loadImage('images.jpg')
    glBindTexture(GL_TEXTURE_2D, texture)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(cameraFrom[0],cameraFrom[1],cameraFrom[2],cameraTo[0],cameraTo[1],cameraTo[2],0,0,1)
    glTranslatef(-j*10+5,8,-i*10+5)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5, 0,  -5)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 5, 0,  -5)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 5,  0,  5)
    glTexCoord2f(0, 1)
    glVertex3f(-5,  0,  5)
    glEnd()
    glPopMatrix()
    
    
def renderLevel():
    global mapArr,moves
    i=0
    j=0
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    gluLookAt(cameraFrom[0],cameraFrom[1],cameraFrom[2],cameraTo[0],cameraTo[1],cameraTo[2],0,0,1)
    while(i<len(mapArr)):
        while(j<len(mapArr[i]) -1):
            if(mapArr[i][j]=="0"):
                pass
            if(mapArr[i][j]=="B"):
                drawCube(cube_list,i,j,brikTex)
            if(mapArr[i][j]=="G"):
                pass
            if(mapArr[i][j]=="C"):
                drawCube(cube_list,i,j,block)
            if(mapArr[i][j]=="CT"):
                drawCube(cube_list,i,j,redBlock)
            if(mapArr[i][j]=="T"):
                drawTarget(i,j)
            j=j+1
        i=i+1
        j=0
    drawPerson()
    glColor3f(1, 1, 1)
    draw_string(70,0,90,"Level:"+str(level))
    draw_string(0,0,90,"Moves:"+str(moves))
    glFlush()
    glutSwapBuffers()


def glInit():
    glClearColor(0.2,0.2,0.8,0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    angle = 60.0
    gluPerspective(angle, SCREEN_SIZE[0]/SCREEN_SIZE[1], 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
def drawBack():
    texture, w, h = loadImage('images.jpg')
    glLoadIdentity()
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-200, 0,  -200)
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 200, 0,  -200)
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 200,  0,  200)
    glTexCoord2f(0, 1)
    glVertex3f(-200,  0,  200)
    glEnd()
    
def main():
    global cube_list,block,brikTex,redBlock
    loadLevel(level)
    pygame.init()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(640,480)
    glutCreateWindow("Sukoban")
    glInit()
    glEnable(GL_TEXTURE_2D)
    cube_list,floor_list = initShapes()
    brikTex, w, h = loadImage('bricks.jpg')
    block, w, h = loadImage('box.jpg')
    redBlock, w, h = loadImage('crate.jpg')
    glutDisplayFunc(renderLevel)
    glutKeyboardFunc(keypress)
    glutSpecialFunc(keypress)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(cameraFrom[0],cameraFrom[1],cameraFrom[2],cameraTo[0],cameraTo[1],cameraTo[2],0,0,1)
    glutMainLoop()
g=0
def animate(x):
    global g
    if cameraFrom[1]>0 and g!=1:
        cameraFrom[1]=cameraFrom[1]-5
        glutTimerFunc(40, animate, 0)
        glutPostRedisplay()
    elif cameraFrom[1]<140 and g==1:
        cameraFrom[1]=cameraFrom[1]+5
        glutTimerFunc(40, animate, 0)
        glutPostRedisplay()
    elif cameraFrom[1]>=140 and g==1:
        g=0
        pass
    else:
        g=1
        loadLevel(level)
        glutTimerFunc(40, animate, 0)
    
def keypress(key,x,y):
    global mapArr,currentPosition,level,targetCount,moves,cameraFrom,cameraTo
    if key == 'x':
        pygame.quit()
        sys.exit()
    if key == 'r':
        loadLevel(level)
    if key=='w':
        cameraFrom[1]=cameraFrom[1]-5
    if key=='s':    
        cameraFrom[1]=cameraFrom[1]+5
    if key=='a':    
        cameraFrom[0]=cameraFrom[0]-5
    if key=='d':    
        cameraFrom[0]=cameraFrom[0]+5
    if key=='q':    
        cameraFrom[2]=cameraFrom[2]-5
    if key=='e':    
        cameraFrom[2]=cameraFrom[2]+5
    if key == GLUT_KEY_UP:
        x = currentPosition[0]
        y = currentPosition[1]
        if(mapArr[x-1][y]=="C" and mapArr[x-2][y]=="0"):
            mapArr[x-2][y]="C"
            mapArr[x-1][y]="0"
            currentPosition[0]=currentPosition[0]-1
            moves=moves+1
        elif(mapArr[x-1][y]=="C" and mapArr[x-2][y]=="T"):
            mapArr[x-2][y]="CT"
            mapArr[x-1][y]="0"
            currentPosition[0]=currentPosition[0]-1
            targetCount=targetCount-1
            moves=moves+1
        elif(mapArr[x-1][y]=="CT" and mapArr[x-2][y]=="T"):
            mapArr[x-2][y]="CT"
            mapArr[x-1][y]="T"
            currentPosition[0]=currentPosition[0]-1
            moves=moves+1
        elif(mapArr[x-1][y]=="CT" and mapArr[x-2][y]=="0"):
            mapArr[x-2][y]="C"
            mapArr[x-1][y]="T"
            targetCount=targetCount+1
            currentPosition[0]=currentPosition[0]-1
            moves=moves+1
        elif(mapArr[x-1][y]=="0" or mapArr[x-1][y]=="T"):
            currentPosition[0]=currentPosition[0]-1
            moves=moves+1

        
    if key == GLUT_KEY_LEFT :
        x = currentPosition[0]
        y = currentPosition[1]
        if(mapArr[x][y-1]=="C" and mapArr[x][y-2]=="0"):
            mapArr[x][y-2]="C"
            mapArr[x][y-1]="0"
            currentPosition[1]=currentPosition[1]-1
            moves=moves+1
        elif(mapArr[x][y-1]=="C" and mapArr[x][y-2]=="T"):
            mapArr[x][y-2]="CT"
            mapArr[x][y-1]="0"
            targetCount=targetCount-1
            currentPosition[1]=currentPosition[1]-1
            moves=moves+1
        elif(mapArr[x][y-1]=="CT" and mapArr[x][y-2]=="T"):
            mapArr[x][y-2]="CT"
            mapArr[x][y-1]="T"
            currentPosition[1]=currentPosition[1]-1
            moves=moves+1
        elif(mapArr[x][y-1]=="CT" and mapArr[x][y-2]=="0"):
            mapArr[x][y-2]="C"
            mapArr[x][y-1]="T"
            targetCount=targetCount+1
            currentPosition[1]=currentPosition[1]-1
            moves=moves+1
        elif(mapArr[x][y-1]=="0" or mapArr[x][y-1]=="T"):
            currentPosition[1]=currentPosition[1]-1
            moves=moves+1

    if key == GLUT_KEY_DOWN:
        x = currentPosition[0]
        y = currentPosition[1]
        if(mapArr[x+1][y]=="C" and mapArr[x+2][y]=="0"):
            mapArr[x+2][y]="C"
            mapArr[x+1][y]="0"
            currentPosition[0]=currentPosition[0]+1
            moves=moves+1
        elif(mapArr[x+1][y]=="C" and mapArr[x+2][y]=="T"):
            mapArr[x+2][y]="CT"
            mapArr[x+1][y]="0"
            targetCount=targetCount-1
            currentPosition[0]=currentPosition[0]+1
            moves=moves+1
        elif(mapArr[x+1][y]=="CT" and mapArr[x+2][y]=="T"):
            mapArr[x+2][y]="CT"
            mapArr[x+1][y]="T"
            currentPosition[0]=currentPosition[0]+1
            moves=moves+1
        elif(mapArr[x+1][y]=="CT" and mapArr[x+2][y]=="0"):
            mapArr[x+2][y]="C"
            mapArr[x+1][y]="T"
            targetCount=targetCount+1
            currentPosition[0]=currentPosition[0]+1
            moves=moves+1
        elif(mapArr[x+1][y]=="0" or mapArr[x+1][y]=="T"):
            currentPosition[0]=currentPosition[0]+1
            moves=moves+1

    if key == GLUT_KEY_RIGHT:
        x = currentPosition[0]
        y = currentPosition[1]
        if(mapArr[x][y+1]=="C" and mapArr[x][y+2]=="0"):
            mapArr[x][y+2]="C"
            mapArr[x][y+1]="0"
            currentPosition[1]=currentPosition[1]+1
            moves=moves+1
        elif(mapArr[x][y+1]=="C" and mapArr[x][y+2]=="T"):
            mapArr[x][y+2]="CT"
            mapArr[x][y+1]="0"
            targetCount=targetCount-1
            currentPosition[1]=currentPosition[1]+1
            moves=moves+1
        elif(mapArr[x][y+1]=="CT" and mapArr[x][y+2]=="T"):
            mapArr[x][y+2]="CT"
            mapArr[x][y+1]="T"
            currentPosition[1]=currentPosition[1]+1
            moves=moves+1
        elif(mapArr[x][y+1]=="CT" and mapArr[x][y+2]=="0"):
            mapArr[x][y+2]="C"
            mapArr[x][y+1]="T"
            targetCount=targetCount+1
            currentPosition[1]=currentPosition[1]+1
            moves=moves+1
        elif(mapArr[x][y+1]=="0" or mapArr[x][y+1]=="T"):
            currentPosition[1]=currentPosition[1]+1
            moves=moves+1

    if(targetCount==0):
        targetCount = -1
        level=level+1
        glutTimerFunc(20, animate, 0)
    glutPostRedisplay()

if __name__ == '__main__':
     main()

    
