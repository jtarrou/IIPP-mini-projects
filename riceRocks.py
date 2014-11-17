# implementation of  RiceRocks
import simplegui
import math
import random

##########################################################
# if you want to initialize with the larger asteroids, please adjust 
# WIDTH to at least 1000 and Height to at least 800
# if music doesn't start, you may have to play the file at http://images.wikia.com/starwars/images/6/61/Imperial_March.ogg 
# once on your computer before loading the game. I need to look into this further
# not sure why it doesn't play. When I play the game on the computer I used
# while writing code it works perfectly, probably because music is already in cache?
#########################################################
# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
#asteroid_set =([])
rock_group = [] 
missile_group = []  
explosion_group = []
my_ast = 1

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# for shot3 but need to put the angle code into shot3 before I use it
#missile_info = ImageInfo([10,10], [20, 20], 3, 50)
#missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
# added asteroids from http://staff.unak.is/andy/gameprogramming0910/bitMapGame/ also from http://images.mzzt.net/
#asteroid_info = ImageInfo([45, 45], [90, 90], 40)
#asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# Deathstar image, I couldn't resist!!
asteroid_info = ImageInfo([32, 32], [64, 64], 40)
asteroid_image = simplegui.load_image("http://images.mzzt.net/deathstar.gif")

# There is only one "info" for all the rest of these large asteroids
# Again, if you're going to use them the canvas needs to be a little larger or it gets crazy crowded.
asteroid2_info = ImageInfo([64, 64], [128, 128])
asteroid2_image = simplegui.load_image("http://staff.unak.is/andy/gameprogramming0910/bitMapGame/asteroid4.png")
asteroid3_image = simplegui.load_image("http://staff.unak.is/andy/gameprogramming0910/bitMapGame/asteroid5.png")
asteroid4_image = simplegui.load_image("http://staff.unak.is/andy/gameprogramming0910/bitMapGame/asteroid2.png")
asteroid5_image = simplegui.load_image("http://staff.unak.is/andy/gameprogramming0910/bitMapGame/asteroid1.png")
asteroid6_image = simplegui.load_image("http://staff.unak.is/andy/gameprogramming0910/bitMapGame/asteroid3.png")


# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# because I got the deathstar I had to go for this alternative sountrack
# thanks to http://starwars.wikia.com/wiki/File:Imperial_March.ogg
soundtrack = simplegui.load_sound("http://images.wikia.com/starwars/images/6/61/Imperial_March.ogg")

# sound assets purchased from sounddogs.com, please do not redistribute
#soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations  
def angle_to_vector(ang):  
    return [math.cos(ang), math.sin(ang)]  
  
def dist(p,q):  
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)  
  
  
def process_sprite_group(canvas, rock_group):  
    for obj in rock_group:  
        obj.draw(canvas)  
        if obj.update():  
            rock_group.remove(obj)  
  
  
def group_collide(group, other_object):  
    all_collisions = 0  
    for obj in set(group):  
        if obj.collide(other_object):  
            group.remove(obj)  
            all_collisions += 1  
    return all_collisions  
  
  
def group_group_collide(group1, group2):  
    all_collisions = 0  
    for obj in set(group1):  
        objcol = group_collide(group2, obj)  
        if objcol:  
            all_collisions += objcol  
            group1.remove(obj)  
    return all_collisions  
  
  
# Ship class  
class Ship:  
  
  
    def __init__(self, pos, vel, angle, image, info):  
        self.pos = [pos[0], pos[1]]  
        self.vel = [vel[0], vel[1]]  
        self.thrust = False  
        self.angle = angle  
        self.angle_vel = 0  
        self.image = image  
        self.image_center = info.get_center()  
        self.image_size = info.get_size()  
        self.radius = info.get_radius()  
          
    def draw(self,canvas):  
        if self.thrust:  
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size, self.pos, self.image_size, self.angle)  
        else:  
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)  
          
    def update(self):  
        # update angle  
        self.angle += self.angle_vel  
          
        # update position  
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH  
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT  
  
        # update velocity  
        if self.thrust:  
            forward = angle_to_vector(self.angle)  
            self.vel[0] += forward[0] * .1  
            self.vel[1] += forward[1] * .1  
              
        self.vel[0] *= .99  
        self.vel[1] *= .99  
  
  
    def set_thrust(self, on):  
        self.thrust = on  
        if on:  
            ship_thrust_sound.rewind()  
            ship_thrust_sound.play()  
        else:  
            ship_thrust_sound.pause()  
         
    def increment_angle_vel(self):  
        self.angle_vel += .05  
          
    def decrement_angle_vel(self):  
        self.angle_vel -= .05  
          
    def shoot(self):  
        global missile_group  
        forward = angle_to_vector(self.angle)  
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]  
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]  
        missile_group.append(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))  
      
    def get_position(self):  
        return self.pos  
      
    def get_radius(self):  
        return self.radius  
      
      
# Sprite class  
class Sprite:  
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):  
        self.pos = [pos[0], pos[1]]  
        self.vel = [vel[0], vel[1]]  
        self.angle = ang  
        self.angle_vel = ang_vel  
        self.image = image  
        self.image_center = info.get_center()  
        self.image_size = info.get_size()  
        self.radius = info.get_radius()  
        self.lifespan = info.get_lifespan()  
        self.animated = info.get_animated()  
        self.age = 0  
        if sound:  
            sound.rewind()  
            sound.play()  
     
    def draw(self, canvas):  
        if self.animated:  
            objcenter=[self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]  
            canvas.draw_image(self.image, objcenter, self.image_size, self.pos, self.image_size, self.angle)  
        else:  
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)  
      
    def update(self):  
        # update angle  
        self.angle += self.angle_vel  
          
        # update position  
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH  
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT  
          
        self.age+=1  
        if self.age > self.lifespan:  
            return True  
        else:  
            return False  
          
    def get_position(self):  
        return self.pos  
      
    def get_radius(self):  
        return self.radius  
      
    def collide(self,other_object):  
        #global explosion_group  
        if dist(self.get_position(), other_object.get_position()) < self.get_radius() + other_object.get_radius():  
            foward = angle_to_vector(self.angle)  
            objpos = [self.pos[0] + self.get_radius(), self.pos[1] + self.get_radius()]  
            kaboom = Sprite(objpos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)  
            explosion_group.append(kaboom)  
            return True  
        else:  
            return False  
    def decrement_angle_vel(self):  
        self.angle_vel -= 0.08  
    def increment_angle_vel(self):  
        self.angle_vel += 0.08  
    
          
# key handlers to control ship     
def keydown(key):  
    if key == simplegui.KEY_MAP['left']:  
        my_ship.decrement_angle_vel()  
    elif key == simplegui.KEY_MAP['right']:  
        my_ship.increment_angle_vel()  
    elif key == simplegui.KEY_MAP['up']:  
        my_ship.set_thrust(True)  
    elif key == simplegui.KEY_MAP['space']:  
        my_ship.shoot()  
          
def keyup(key):  
    if key == simplegui.KEY_MAP['left']:  
        my_ship.increment_angle_vel()  
    elif key == simplegui.KEY_MAP['right']:  
        my_ship.decrement_angle_vel()  
    elif key == simplegui.KEY_MAP['up']:  
        my_ship.set_thrust(False)  
          
# mouseclick handlers that reset UI and conditions whether splash image is drawn  
def click(pos):  
    global started, lives, score, my_ship, my_ast  
    center = [WIDTH / 2, HEIGHT / 2]  
    size = splash_info.get_size()  
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)  
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)  
    if (not started) and inwidth and inheight:  
        started = True  
        lives = 3  
        score = 0  
        my_ast = 1  
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)  
        soundtrack.rewind()  
        soundtrack.play()  
  
  
def draw(canvas):  
    global time, started, lives, rock_group, missile_group, explosion_group, score  
      
    # animiate background  
    time += 1  
    wtime = (time / 4) % WIDTH  
    center = debris_info.get_center()  
    size = debris_info.get_size()  
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])  
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))  
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))  
  
    # draw title
    canvas.draw_text("RICE ROCKS!", (220, 60), 60, "Red")
          
    
    # draw score
    canvas.draw_text("Score", (WIDTH - 120, 85), 24, "Aqua")
    canvas.draw_text(str(score), (WIDTH - 80, 120), 32, "Aqua")
    
    # draw lives
    canvas.draw_text("Lives", (60, 85), 24, "Aqua")
    canvas.draw_text(str(lives), (100, 120), 32, "Aqua")
  
    # draw ship and sprites  
    my_ship.draw(canvas)  
    process_sprite_group(canvas, rock_group)  
    process_sprite_group(canvas, missile_group)  
    process_sprite_group(canvas, explosion_group)  
      
    # update ship and sprites  
    my_ship.update()  
  
    # draw splash screen if not started  
    if not started:  
        canvas.draw_image(splash_image, splash_info.get_center(),   
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],   
                          splash_info.get_size())  
        return  
    
    # lives and score counters
    if group_collide(rock_group, my_ship):  
        lives -= 1  
    if group_group_collide(rock_group, missile_group):  
        score += 1
    if score >= 1:
        canvas.draw_text("Use the force, Luke!", (320, 120), 22, "White")
    if score >= 5:
        canvas.draw_text("The force is strong with this one.", (260, 570), 22, "Red")
    if len(rock_group) >= 12:
        canvas.draw_text("I have you now!", (360, 550), 22, "Red")
        
    
    # game over man, game over      
    if lives == 0:  
        started = False  
        rock_group = []  
        explosion_group = []  
                  
# timer handler that spawns a rock      
def rock_spawner():  
    global rock_group, my_ast  
    my_ast *= 1.05  
    if len(rock_group) >= 12 or not started:  
        return  
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]  
    
    # keep asteroid from spawning on top of ship
    while dist(my_ship.get_position(),rock_pos) < 200:  
            rock_pos=[random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]  
    rock_vel = [my_ast * random.random() * .6 - .3, my_ast * random.random() * .6 - .3]  
    rock_avel = random.random() * .2 - .1  
    rock_group.append(Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info))  
              
# initialize stuff  
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)  

# initialize ship and two sprites  
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)  
  
# register handlers  
frame.set_keyup_handler(keyup)  
frame.set_keydown_handler(keydown)  
frame.set_mouseclick_handler(click)  
frame.set_draw_handler(draw)  

timer = simplegui.create_timer(1000.0, rock_spawner)  

# get things rolling 
soundtrack.play()
timer.start()  
frame.start()  
