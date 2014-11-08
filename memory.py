# implementation of card game - Memory

import simplegui
import random
number = []
exposed = []
state = 0
turn = 0
init_num = 0
next_num = 0


#Model the deck of numbers used in Memory as a list 
#consisting of 16 numbers with each number lying in 
#the range [0,8) and appearing twice. 
def new_game():
    global state, exposed, turn, number
    number = [i for i in xrange(0, 8)]*2 
    random.shuffle(number) #step 3
    exposed = [False]*16
    state = 0
    turn = 0 
                  
   
#define event handlers
def click(pos):
    global state, exposed, number, init_num, next_num, turn
    cards = pos[0]//50 #for separation based on pixels
    if not exposed[cards]:
        exposed[cards] = True
        if state == 0:        
            state = 1
            init_num = cards
        elif state == 1:
            next_num = cards
            state = 2
        elif state == 2:
            if number[init_num] != number[next_num]:
                exposed[init_num] = False
                exposed[next_num] = False
            init_num = cards
            state=1
        turn = turn + 1
        
#number are logically 50x100 pixels in size    
def draw(canvas):
    global turn, number, init_num, next_num
    for i in xrange(16):
        if exposed[i]:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Black", "Red")
            canvas.draw_text(str(number[i]), (i*50+11, 69), 55, "Black")
            ##Trying to get it to change the successful attempts to white, 
            ##Leaving the unsuccessful attempts black, but it's skipping 
            ##stright to the white. 
            if init_num == next_num:
               canvas.draw_text(str(number[i]), (i*50+11, 69), 55, "White")
        else:
            canvas.draw_polygon([[i*50, 0], [(i+1)*50, 0], [(i+1)*50, 100], [i*50, 100]], 1, "Black", "Green")
    label.set_text("Turns = " + str(turn))

#create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game, 200)
label = frame.add_label("Turns = 0")

#register event handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

#get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
