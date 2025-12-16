import pygame
import math

def window_blit(self):
    if self.c[0]*(window/window_sz) + (window_sz-window)/2 + center_xdis*(window/window_sz) -(5*(window/window_sz))< window_sz and self.c[0]*(window/window_sz) + (window_sz-window)/2 + center_xdis*(window/window_sz) + (5*2*(window/window_sz)) > 0 and self.c[1]*(window/window_sz) + (window_sz-window)/2 + center_ydis*(window/window_sz) - (5*(window/window_sz)) < window_sz and self.c[1]*(window/window_sz) + (window_sz-window)/2 + center_ydis*(window/window_sz) + (5*2*(window/window_sz))> 0:
            new_surface = pygame.transform.scale(self.surf, (5*2*(window/window_sz), 5*2*(window/window_sz)))
            new_surface = new_surface.convert_alpha()
            screen.blit(new_surface,(self.c[0]*(window/window_sz) + ((window_sz-window)/2)*(window/window_sz) + center_xdis*(window/window_sz) - 5*(window/window_sz),self.c[1]*(window/window_sz) + (window_sz-window)/2 + center_ydis*(window/window_sz) - 5*(window/window_sz)))
    
def window2(self):
    width = pointgaps/2
    new_coords = [window_sz*(mag*(self.c[0] - width/2 - center_xdis) + 0.5),window_sz*(mag*(self.c[1] - width/2 - center_ydis) + 0.5)]
    if new_coords[0] > 800 or new_coords[0] < 0 or new_coords[1] > 800 or new_coords[1] < 0: pass
    else:
        new_surface = pygame.transform.scale(self.surf, (width*mag*window_sz, width*mag*window_sz))
        new_surface = new_surface.convert_alpha()
        screen.blit(new_surface,new_coords)
    
def vectorcomponent(angle, magnitude, XorY):
    if XorY == "y":
        angle -= 90
        if angle < 0:
            angle += 360
    dis = math.cos(math.radians(angle)) * magnitude
    return dis

def abswin_convert(point,original,xory):
    win_ratio = window/window_sz
    if original == "abs":
        if xory == "x":
            new_point = point*(win_ratio) + (window_sz-window)/2 + center_xdis*(win_ratio)
        else:
            new_point = point*(win_ratio) + (window_sz-window)/2 + center_ydis*(win_ratio)
    elif original == "win":
        if xory == "x":
            new_point = (point - center_xdis)*(win_ratio)
    #        new_point = (point - center_xdis*(win_ratio) - (window_sz-window)/2)/(win_ratio)
        else:
            new_point = (point - center_ydis)*(win_ratio)
    #        new_point = (point - center_ydis*(win_ratio) - (window_sz-window)/2)/(win_ratio)
    return new_point
    

def angleturn(point1,point2):
    xdis = point1[0] - point2[0]
    ydis = point1[1] - point2[1]
    if not xdis:
        if ydis >= 0:
            Angle = 270
        else:
            Angle = 90
    else:
        Angle = math.degrees(math.atan(ydis/xdis))
    if xdis <= 0 and ydis <= 0:
        Angle = 0 + Angle
        #print("UpLeft")
    elif xdis <= 0 and ydis >= 0:
        Angle = 360 + Angle
        #print("DownLeft")
    elif xdis >= 0 and ydis >= 0:
        Angle = 180 + Angle
        #print("DownRight")
    elif xdis >= 0 and ydis <= 0:
        Angle = 180 + Angle
        #print("UpRight")
    return Angle

def dis(point1,point2):
    dis = math.sqrt((point1[0]-point2[0])**2 + (point1[1] - point2[1])**2)
    return dis

def Gravity(M,m,d):
    Force = (M*m*(6.7*(10**-11)))/(d**2)
    return Force

def vectoradd(v1,v2):
    i = v1[0] + v2[0]
    j = v1[1] + v2[1]
    return [i,j]

def vectormag(v):
    IvI = math.sqrt(v[0]**2 + v[1]**2)
    return IvI

def GravityUpdate(p):
    sqr = p.surf
    vectors = []
    for m in masses:
        distance = dis(m.c,p.c)
        magnitude = Gravity(m.mass,1,distance)
        angle = angleturn(p.c,m.c)
        vectors.append([vectorcomponent(angle,magnitude,"x"),vectorcomponent(angle,magnitude,"y")])
        
    distance = dis(masses[1].c,p.c)
    magnitude = 4*(math.pi**2)*distance*(1/((365*24*60*60)**2))
    angle = angleturn(masses[1].c,p.c)
    vectors.append([vectorcomponent(angle,magnitude,"x"),vectorcomponent(angle,magnitude,"y")])
    
    resultant = [0,0]
    for v in vectors:
        resultant = [resultant[0]+v[0],resultant[1]+v[1]]
        
    #print(vectors,resultant)
    resultant_angle = angleturn([0,0],resultant)
    resultant_magnitude = math.sqrt(resultant[0]**2 + resultant[1]**2)
    p.vector = resultant
    
    brightness = int((1/sens*resultant_magnitude))
    lagrange = False
    if brightness > 255: brightness = 255
    if brightness <= 1: lagrange = True
    
    sqr.fill(pygame.Color(brightness,brightness,brightness))
    if lagrange: sqr.fill("red")
class PointVector:
    def __init__(self,coords,vector,surf):
        self.c = coords
        self.vector = vector
        self.surf = basic_square
        
class PointMass:
    def __init__(self,coords,mass,vel):
        self.c = coords
        self.mass = mass
        self.vel = vel


pygame.init()
void = pygame.Surface((1000,1000))
window_sz = 600
window = 800
screen = pygame.display.set_mode((window_sz,window_sz))
pygame.display.set_caption("Vector Map")
clock = pygame.time.Clock()
tick_freq = 60
per_tick = 1/tick_freq
center_ychange = 0
center_xchange = 0
mag_change = 1
sens = 1/100000
sm = per_tick*60*60*24*365 #speed multiplier
t = 0

points = []
pointrange = 300
pointgaps = 0.05*149597870700
mag = (pointgaps*pointrange)**-1
midpoint = (pointrange*pointgaps)/2
center_xdis = midpoint
center_ydis = midpoint
masses = [PointMass([midpoint,midpoint + 0.5],6*10**24,[0,29750]),PointMass([midpoint + (149597870700), midpoint + 0.5],2*10**30,[0,0])]
basic_square = pygame.Surface((10,10))
basic_square.fill("red")
for iy in range(0,pointrange):
    points.append([])
    for ix in range(0,pointrange):
        points[-1].append(PointVector([pointgaps*ix,pointgaps*iy],[0,0],basic_square))

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
                    center_ychange = -1/mag
                if event.key == pygame.K_s:
                    center_ychange = 1/mag
                if event.key == pygame.K_a:
                    center_xchange = -1/mag
                if event.key == pygame.K_d:
                    center_xchange = 1/mag
                if event.key == pygame.K_o:
                    mag_change = 0.95
                if event.key == pygame.K_i:
                    mag_change = 1.05
                if event.key == pygame.K_k:
                    sens *= 5
                if event.key == pygame.K_l:
                    sens /= 5
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    center_ychange = 0
                if event.key == pygame.K_s:
                    center_ychange = 0
                if event.key == pygame.K_a:
                    center_xchange = 0
                if event.key == pygame.K_d:
                    center_xchange = 0
                if event.key == pygame.K_o:
                    mag_change = 1
                if event.key == pygame.K_i:
                    mag_change = 1
    mag = mag*mag_change
    center_xdis += center_xchange/tick_freq
    center_ydis += center_ychange/tick_freq
    screen.blit(void,(0,0))
    
    for rows in points:
        for p in rows:
            GravityUpdate(p)
            window2(p)
            
    for m1 in masses:
        forces = []
        for m2 in masses:
            if m1 != m2:
                distance = dis(m1.c,m2.c)
                magnitude = Gravity(m1.mass,m2.mass,distance)
                angle = angleturn(m1.c,m2.c)
                forces.append([vectorcomponent(angle,magnitude,"x"),vectorcomponent(angle,magnitude,"y")])
        resultant = [0,0]
        for F in forces:
            resultant = [resultant[0]+F[0],resultant[1]+F[1]]
        acceleration = [sm*resultant[0]/m1.mass,sm*resultant[1]/m1.mass]
        m1.vel = [m1.vel[0] + acceleration[0],m1.vel[1] + acceleration[1]]
        m1.c = [m1.c[0] + sm*m1.vel[0],m1.c[1] + sm*m1.vel[1]]
    
    pygame.display.update()
    clock.tick(tick_freq)