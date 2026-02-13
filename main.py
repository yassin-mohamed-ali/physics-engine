import pygame
import math
import random
pygame.init()
clock = pygame.time.Clock()
G = 6.674*(10**2)
font = pygame.font.SysFont(None, 25)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("physics")
class Planet:
    def __init__(self,x,y,mass,volume,color, vx=0, vy=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.density = mass/volume
        self.color = color
        self.volume = volume
        self.radius = (3 * (self.volume / 1e9) / (4 * math.pi)) ** (1/3)
        self.vx=vx
        self.vy=vy
        self.momentum = ((vx+vy)/2)*mass
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
def distance(p1,p2):
    return math.sqrt(((p1.y-p2.y)**2)+(p1.x-p2.x)**2)
def force(p1,p2):
    return (G * p1.mass * p2.mass) / ((distance(p1,p2))**2)
def acceleration(p, force):
    return force/p.mass
def is_colliding(p1, p2):
    return distance(p1, p2) <= (p1.radius + p2.radius)
running = True
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
size_refrence = font.render('this is 100 km', True, WHITE)
planets = [Planet(random.randint(10,screen.get_width()-10),random.randint(10,screen.get_height()-10),1e3,1e15,RED),Planet(random.randint(10,screen.get_width()-10),random.randint(10,screen.get_height()-10),1e5,1e15,RED)]
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(100)/1000
    screen.fill(BLACK)
    pygame.draw.line(screen,WHITE,(10,10),(110,10))
    screen.blit(size_refrence,(10,20))
    
    if len(planets) == 2 and is_colliding(planets[0],planets[1]):
        p1, p2 = planets
        new_mass = p1.mass + p2.mass
        new_volume = p1.volume + p2.volume
        new_x = (p1.x * p1.mass + p2.x * p2.mass) / new_mass
        new_y = (p1.y * p1.mass + p2.y * p2.mass) / new_mass

        new_vx = (p1.vx * p1.mass + p2.vx * p2.mass) / (p1.mass + p2.mass)
        new_vy = (p1.vy * p1.mass + p2.vy * p2.mass) / (p1.mass + p2.mass)
        new_vx += random.uniform(-1, 1)
        new_vy += random.uniform(-1, 1)

        print(new_vx,new_vy)
        planets = [Planet(new_x, new_y, new_mass, new_volume, RED, new_vx, new_vy)]
    if len(planets) == 2:
        f = force(planets[0], planets[1])
        for p in planets:
            ps = [x for x in planets if x != p][0]
            d = distance(p, ps)
            dx = ps.x - p.x
            dy = ps.y - p.y
            dir_x = dx / d
            dir_y = dy / d
            ax = (f / p.mass) * dir_x
            ay = (f / p.mass) * dir_y
            p.vx += ax * dt
            p.vy += ay * dt
    for p in planets:
        p.x += p.vx * dt
        p.y += p.vy * dt
        factor = random.uniform(0.9,0.99)
        p.vx*= factor
        p.vy*= factor
        p.draw()    
    pygame.display.update()
    
    clock.tick(100)
pygame.quit()