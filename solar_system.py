#libraries
import pygame as pg
import math
from random import randint
#initialise
pg.init()

#create a window
screen_info= pg.display.Info()
width = screen_info.current_w
height = screen_info.current_h
WINDOW = pg.display.set_mode((width,height))
pg.display.set_caption('Solar System Simulator')

#color
black = (0,0,0)
yellow = (255,255,0)
gray = (128,128,128)
yellowish_white = (255,255,237)
blue = (0,0,255)
red = (188,39,50)
orange = (255,165,0)
NAME_TEXT_COLOR = (111,236,123)
DIST_TEXT_COLOR = (56,190,255)
#font
NAME_TEXT = pg.font.SysFont(name = 'TimesRoman', size = 18, bold = True)
DIST_TEXT = pg.font.SysFont(name = 'Sans', size = 16,  bold = True)
SUN_NAME_COLOR=(144,128,254)
SUN_TEXT_COLOR=(54,32,12)

class SolarSystemBodies: 
    AU = 1.496e11
    SCALE = 230/AU
    G = 6.6743e-11
    time_step = 24*3600
    def __init__(self, name, color, x, y, mass, radius):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius

        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        self.orbit = []
    
    # method1 to draw bodies on the simulator
    def draw_body(self, WINDOW):
        x = self.x*SolarSystemBodies.SCALE + width//2
        y = self.y*SolarSystemBodies.SCALE + height//2
        pg.draw.circle(surface=WINDOW,color = self.color, center=(x,y), radius=self.radius)

        if not self.sun:
            name_text = NAME_TEXT.render(self.name,True,NAME_TEXT_COLOR)
            WINDOW.blit(name_text,(x-40,y-55))
            dist_text = DIST_TEXT.render(f"{round(self.distance_to_sun/(3e8*60),3)}It-min",True,DIST_TEXT_COLOR)
            WINDOW.blit(dist_text,(x-40,y-35))
        else:
            name_text = NAME_TEXT.render(self.name,True,SUN_NAME_COLOR)
            WINDOW.blit(name_text,(x-40,y-80))
            dist_text = DIST_TEXT.render(f"{round(self.x/3e8,3), round(self.y/3e9,3)}It-sec",True,DIST_TEXT_COLOR)
            WINDOW.blit(dist_text,(x-40,y-55))
            
    #METHOD- TO TRACK ORBITS
    def track_orbit(self,WINDOW):
        if len(self.orbit) > 1:
            centered_points = []
            for (x,y) in self.orbit:
                x = x*self.SCALE + width//2
                y = y*self.SCALE + height//2
                centered_points.append((x,y))
            pg.draw.lines(surface=WINDOW,color=self.color,closed=False,points=centered_points,width=2)

    #method to combine bodies
    def draw(self, WINDOW, track = True):
        self.draw_body(WINDOW)
        if track:
            self.track_orbit(WINDOW)


    #method2 - calc gravitational force
    def gravitational_force(self,ss_body):
        #F= GMm/r^2
        x_diff = ss_body.x - self.x
        y_diff = ss_body.y - self.y
        distance  = math.sqrt(x_diff**2 + y_diff**2)
        if ss_body.sun:
            self.distance_to_sun = distance
        g_force = self.G*self.mass*ss_body.mass / distance**2
        theta = math.atan2(y_diff, x_diff)
        f_x = g_force*math.cos(theta)
        f_y = g_force*math.sin(theta)
        return f_x, f_y
    
    #method3 - update the position
    def updated_position(self, ss_bodies):
        net_fx, net_fy = 0, 0
        for ss_body in ss_bodies:
            if self != ss_body:
                f_x, f_y = self.gravitational_force(ss_body)
                net_fx += f_x
                net_fy += f_y
        self.x_vel += net_fx / self.mass*self.time_step
        self.y_vel += net_fy / self.mass*self.time_step
        self.x += self.x_vel*self.time_step
        self.y += self.y_vel*self.time_step
        self.orbit.append((self.x,self.y))

#stars list with color, center, radius
stars_list = [
    {
        'color' : (randint(190,255), randint(190,255),randint(190,255)),
        'center' : (randint(5,width-5),randint(5,height-5)),
        'radius': (randint(1,2))

    }
    for star in range(400)
]
print(stars_list)
#function to draw stars
def draw_stars(stars_list):
    for star in stars_list:
        pg.draw.circle(WINDOW, star['color'],star['center'],star['radius'])

#create a simulation
run = True
paused = False
sun = SolarSystemBodies("sun", yellow, 0,0 ,1.989e30,30)
sun.sun = True
mercury = SolarSystemBodies("mercury",orange, 0.39*SolarSystemBodies.AU, 0, 0.33e24 , 6)
mercury.y_vel = -47.4e3
venus = SolarSystemBodies("venus", yellowish_white, 0.72*SolarSystemBodies.AU,0,4.87e24,14)
venus.y_vel = -35e3 
earth = SolarSystemBodies("earth", blue, 1*SolarSystemBodies.AU, 0, 5.97e24, 15)
earth.y_vel = -29.8e3
mars = SolarSystemBodies("Mars", red, 1.52*SolarSystemBodies.AU,0,0.642e24,8)
mars.y_vel = -24.1e3

FPS = 60
clock = pg.time.Clock()

while run:
    clock.tick(FPS)
    WINDOW.fill(black)
    draw_stars(stars_list)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
             run = False
            elif event.key == pg.K_SPACE:
             paused = not paused
    if not paused:
         ss_bodies = [sun, mercury, venus,earth,mars]
         for body in ss_bodies:
            body.updated_position(ss_bodies)
            body.draw(WINDOW, track=True)
    pg.display.update()
#quit the pygame
pg.quit()