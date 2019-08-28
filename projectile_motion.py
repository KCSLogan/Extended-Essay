from math import *  #note trigonometry is measured in radians
from time import *
import pygame as pyg

#Functions

def getAcc(x,z,y,Me,Mm,G,d):    #Gets the acceleration due to gravity given
                            #the point in space and the g-fields at that point.
    az = -G*z*(((Me)/((x**2+z**2+y**2)**(3/2)))+((Mm)/((x**2+z**2+(d-y)**2)**(3/2))))
    ax = -G*x*(((Me)/((x**2+z**2+y**2)**(3/2)))+((Mm)/((x**2+z**2+(d-y)**2)**(3/2))))
    ay = G*((((d-y)*Mm)/((x**2+z**2+(d-y)**2)**(3/2)))-((y*Me)/((x**2+z**2+y**2)**(3/2))))
    return (ax,az,ay)

def getVel(dt,x,z,y,vx,vz,vy,ax,az,ay):   #Gets the velocities given the acceleration in the previous
                                #instance (dt)
    vx = vx+(ax*dt)
    vz = vz+(az*dt)
    vy = vy+(ay*dt)
    return(vx,vz,vy)

def getPos(dt,x,z,y,vx,vz,vy):      #Gets the position given the velocity in the previous
                                #instance (dt)
    return((x+(vx*dt)),(z+(vz*dt)),(y+(vy*dt)))

def toPygame(earthPos, coords): #Converting maths coords into appropriate pygame coords.
                                #Passes in the pixel position of the earth for translation
                                #reference.
    newCoords = []
    newCoords.append((earthPos[0]+(k*coords[0])))   #Multiplying by k converts spatial
    newCoords.append((earthPos[1]-(k*coords[1])))   #coordinates to pixel coordinates.
    return newCoords

def listToInt(l):   #Converts a list of floats to a list of integers
    newL = []
    for i in range(len(l)):
        newL.append(int(l[i]))
    return newL

def offsetCoords(coords,xOff,yOff):
    return[coords[0]+xOff,coords[1]+yOff]

#Variables (and initial conditions)

dt = 0.05    #System constants
Me = 81 #6*10**24
Mm = 1 #7.3*10**22
G = 10 #6.67*10**(-11)
d = 100 #360000000
Re = 3.7 #6400000
Rm = 1  #1700000
T =  5  #seconds
omg = (2*3.14)/T #rad/s

w = 800     #Screen width and height
h = 800

k = (0.6*h)/d   #1m = kpx

x = 0      #Initial object position, velocity and acceleration
z = 0
y = Re + 20

vx = 0
vz = 0
vy = 0

ax = 0
az = 0
ay = 0

white = (255,255,255)   #Color RGB definitions (because pygame lazy)
black = (0,0,0)
blue = (0,0,230)
red = (255,0,0)

xOff = 0    #Variables for screen manipulation (scrolling and zooming)
yOff = 0

#Main

check = pyg.init()

disp = pyg.display.set_mode((w,h)) #Returns a pygame.SurfaceObject
pyg.display.set_caption('Earth-Moon Projectile Motion')
earthPos = listToInt([w/2,(0.8*h)])
moonPos = listToInt([w/2,0.2*h])

disp.fill(white)

gameExit = False

while not gameExit:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            gameExit = True

    t1 = perf_counter()

    #Delete object circle (draw over in white)
    pyg.draw.circle(disp,white,listToInt(toPygame(earthPos,[x,y])),3)

    #Redraw Earth and Moon
    visual_Re = int(Re*k)
    visual_Rm = int(Rm*k)
    
    if(visual_Re<4):
        visual_Re = 4
    if(visual_Rm<2):
        visual_Rm = 2
    pyg.draw.circle(disp, blue, earthPos, visual_Re)
    pyg.draw.circle(disp, black, moonPos, visual_Rm)
    pyg.display.update()
    
    #Get accelerations
    accs = getAcc(x,z,y,Me,Mm,G,d)
    #accs = [0,0,0]
    ax = accs[0]
    az = accs[1]
    ay = accs[2]

    #Get velocities
    vels = getVel(dt,x,z,y,vx,vz,vy,ax,az,ay)
    vx = vels[0]
    vz = vels[1]
    vy = vels[2]

    #Get positions
    pos = getPos(dt,x,z,y,vx,vz,vy)
    x = pos[0]
    z = pos[1]
    y = pos[2]

    #Draw object circle
    pyg.draw.circle(disp,red,listToInt(toPygame(earthPos,[x,y])),3)
    pyg.display.update()

    #Check object has not collided
    if((x**2)+(y**2)<=((Re)**2)) or ((x**2)+((d-y)**2)<=((Rm)**2)):
        print("x^2: "+str(x**2)+"\n y^2: "+str(y**2)+"\n (d-y)^2:"+str((d-y)**2)+"\n Re^2: "+str(Re**2)+"\n Rm^2: "+str(Rm**2))
        gameExit = True
    else:
        pass

    #Check computation times
    t2 = perf_counter()
    t = t2-t1

    if(dt-t >= 0):
       sleep(dt-t)
    else:
        pass
    
pyg.quit()
quit()
