import simplegui
import random

# initialize globals 
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 12
PAD_WIDTH = 8
PAD_HEIGHT = 80
EDGE = True

# helper function: spawns ball, updates ball's position & velocity vectors
# if right is True, ball's velocity is upper right, else (meaning left is true, or EDGE is False, 
# velocity is upper left
def spawn_ball(right):
    global ball_pos, ball_vel # vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if right == True:
        ball_vel = [random.randrange(2, 4), -random.randrange(1, 3)]
    else:
        ball_vel = [-random.randrange(2, 4), -random.randrange(1, 3)]
    
# event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2, EDGE
    paddle1_pos, paddle2_pos = (HEIGHT - PAD_HEIGHT)/2, (HEIGHT - PAD_HEIGHT)/2
    paddle1_vel = paddle2_vel = 0
    score1, score2 = 0, 0 # these are ints
    EDGE = not EDGE
    spawn_ball(EDGE)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    # draw scores
    c.draw_text(str(score1), (185, 40), 40, "Red")
    c.draw_text(str(score2), (400, 40), 40, "Blue")
 
    # update paddle's position, keep paddle from wandering off into nowhere
    if 0 <= (paddle1_pos + paddle1_vel) <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if 0 <= (paddle2_pos + paddle2_vel) <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel   
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw ball 
    c.draw_circle(ball_pos, BALL_RADIUS, 0.1, "White", "White")
    
    # update ball
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if paddle1_pos <= ball_pos[1] <= (paddle1_pos + PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            spawn_ball(True)
            score2 += 1
    if ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if paddle2_pos <= ball_pos[1] <= (paddle2_pos + PAD_HEIGHT):
            ball_vel[0] = - 1.1 * ball_vel[0]
        else:
            spawn_ball(False)
            score1 += 1
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if ball_pos[1] >= (HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw paddles
    c.draw_line([PAD_WIDTH/2, paddle1_pos],[PAD_WIDTH/2, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "Red")
    c.draw_line([WIDTH - PAD_WIDTH/2, paddle2_pos],[WIDTH - PAD_WIDTH/2, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "Blue")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    vel = 5
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel   
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0  
        
def restart_cmd():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart_cmd, 100)

# start frame
frame.start()
new_game()
