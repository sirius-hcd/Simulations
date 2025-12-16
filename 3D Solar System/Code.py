### Celestial Sphere Test ####

import math
import pygame

class Point():
    def __init__(self,x,y,z):
        self.x = tometre(x)
        self.y = tometre(y)
        self.z = tometre(z)
        self.vel = [0,0,0]
        
class Object():
    def __init__(self,name,coords,velocity,radius,colour,mag):
        self.name = name
        self.surf = pygame.image.load(f"Graphics\Solar System\{name}.png").convert_alpha()
        self.x = tometre(coords[0])
        self.y = tometre(coords[1])
        self.z = tometre(coords[2])
        self.r = tometre(radius)
        self.i = tomps(velocity[0])
        self.j = tomps(velocity[1])
        self.k = tomps(velocity[2])
        self.col = colour
        self.mag = mag
        
def tometre(length):
    try:
        return int(length)
    except:
        if length[-2:] == "au":
            return float(length[:-2])*1.5*(10**11)
        elif length[-2:] == "ly":
            return float(length[:-2])*3*(10**8)*365*24*60*60
        elif length[-2:] == "km":
            return float(length[:-2])*1000
        elif length[-1:] == "m":
            return float(length[:-1])
        
def tomps(length):
    try:
        return int(length)
    except:
        if length[-3:] == "mps" and length[-4:] != "kmps":
            return float(length[:-3])
        elif length[-1:] == "c":
            return float(length[:-1])*3*(10**8)
        elif length[-4:] == "kmps":
            return float(length[:-4])*1000
        elif length[-4:] == "kmph":
            return float(length[:-4])*1000*(1/3600)
        elif length[-5:] == "aupsy": #au per solar year
            period = math.sqrt(float(length[:-5])**3)*365*24*60*60
            circ = 2*math.pi*(float(length[:-5])*1.5*(10**11))
            return circ/period
        elif length[-4:] == "aups":
            return float(length[:-4])*1.5*(10**11)
def rtd(radians):
    degrees = 360*(radians/(2*math.pi))
    return degrees
    
def dtr(degrees):
    radians = (2*math.pi)*(degrees/360)
    return radians

def dis(n1,n2):
    dx = n1.x - n2.x
    dy = n1.y - n2.y
    dz = n1.z - n2.z
    d = math.sqrt(dx**2 + dy**2 + dz**2)
    return d
        
def atw(angle):
    window_distance = screen_width*angle/fov
    return window_distance
    
def vectorcomponent(angle, magnitude, XorY):
    if XorY == "y":
        angle -= 90
        if angle < 0:
            angle += 360
    dis = math.cos(math.radians(angle)) * magnitude
    return dis

def CS_Display(peripheral_object):
    O = Observer
    P = peripheral_object
    try: delta = rtd(math.atan(math.sqrt((P.y - O.y)**2 + (P.x - O.x)**2)/(P.z - O.z)))
    except: delta = 90
    cov_dis = atw(delta)
    alpha = math.atan((P.y - O.y)/(P.x - O.x)) + roll_angle
    di = cov_dis*math.cos(alpha)
    if (P.x - O.x) >= 0: i = (screen_width/2)+abs(di)
    elif (P.x - O.x) < 0: i = (screen_width/2)-abs(di)
    dj = cov_dis*math.sin(alpha)
    if (P.y - O.y) >= 0: j = (screen_width/2)+abs(dj)
    elif (P.y - O.y) < 0: j = (screen_width/2)-abs(dj)
    app_rad = atw(rtd(math.atan(P.r/dis(O,P))))
    if app_rad < 1:
        surf = pygame.Surface((1,1))
        appmag = 5*math.log10((dis(O,P)/(1.5*(10**11)))) + P.mag
        brightness = round((255/2)*(-appmag/7))
        surf.fill(pygame.Color(brightness,brightness,brightness))
    else:
        surf = pygame.transform.scale(P.surf,(app_rad*2,app_rad*2))
    screen.blit(surf,(i-app_rad,j-app_rad))
 
pygame.init()
screen_width = 1000
screen = pygame.display.set_mode((screen_width,screen_width))
pygame.display.set_caption("3D Solar System")

cov = Point(0,0,0)
roll_angle = 0
Observer = Point("1.000000000000001au",0,"6000km")
void = pygame.Surface((1000,1000))
Earth = Object("Earth",["1au",0,0],[0,"1aupsy",0],"6000km","Blue",-3.99)
Sun = Object("Sol",[0,0,0],[0,0,0],"695700km","White",-26.7)
Bodies = [Earth,Sun]

clock = pygame.time.Clock()
tick_freq = 120
per_tick = 1/tick_freq
sens = 1/100000
smi = 5 #speed multiplier index
sm = [1,10,100,"1kmps","10kmps","100kmps","1000kmps","10000kmps","0.1c","0.25c","0.5c","0.75c","1c","10c","0.5aups","1aups"] #speed multipliers
fovs = [0.1*60**-2,60**-2,60**-1,0.5,1,5,10,20,30,45,60,75,80,90,100,120,150,180]
fovi = 9
t = 0
tickspeed = 0

running = True
print("running")
while running:
    mp = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    Observer.vel = [Observer.vel[0],-tomps(sm[smi]),Observer.vel[2]]
                if event.key == pygame.K_s:
                    Observer.vel = [Observer.vel[0],tomps(sm[smi]),Observer.vel[2]]
                if event.key == pygame.K_a:
                    Observer.vel = [-tomps(sm[smi]),Observer.vel[1],Observer.vel[2]]
                if event.key == pygame.K_d:
                    Observer.vel = [tomps(sm[smi]),Observer.vel[1],Observer.vel[2]]
                if event.key == pygame.K_q:
                    Observer.vel = [Observer.vel[0],Observer.vel[1],-tomps(sm[smi])]
                if event.key == pygame.K_e:
                    Observer.vel = [Observer.vel[0],Observer.vel[1],tomps(sm[smi])]
                if event.key == pygame.K_r:
                    roll_angle += 1
                if event.key == pygame.K_PERIOD:
                    smi += 1
                    if smi > len(sm)-1: smi -= 1
                if event.key == pygame.K_COMMA:
                    smi -= 1
                    if smi < 0: smi = 0
                if event.key == pygame.K_i:
                    fovi -= 1
                    if fovi < 0: fovi = 0
                if event.key == pygame.K_o:
                    fovi += 1
                    if fovi > len(fovs)-1: fovi -= 1
                    
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    Observer.vel = [Observer.vel[0],0,Observer.vel[2]]
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    Observer.vel = [0,Observer.vel[1],Observer.vel[2]]
                if event.key == pygame.K_q or event.key == pygame.K_e:
                    Observer.vel = [Observer.vel[0],Observer.vel[1],0]
    
    fov = fovs[fovi]
    screen.blit(void,(0,0))
    Observer.x += Observer.vel[0]
    Observer.y += Observer.vel[1]
    Observer.z += Observer.vel[2]
    
    for B in Bodies:
        CS_Display(B)
        B.x += B.i*tickspeed
        B.y += B.j*tickspeed
        B.z += B.k*tickspeed
    
    pygame.display.update()
    clock.tick(tick_freq)