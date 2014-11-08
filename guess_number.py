# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables used in your code here
count_limit = 0
secret_number = 0
game = " "
# helper function to start and restart the game

def range100():
    # button that changes the range to [0,100) and starts a new game 
    global secret_number
    global count_limit
    global game
    # 0-101 so that 1 and 100 are possibilities
    secret_number = random.randrange(0, 101)
    game = 1
    count_limit = 7
    print " "
    print "New Game. Range is 1 to 100"
    print "Please guess a number."
    print "You have %s guesses remaining." %count_limit
    
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number
    global count_limit
    global game
    # same explaination as above
    secret_number = random.randrange(0, 1001)
    game = 0
    count_limit = 10
    print " "
    print "New Game. Range is 1 to 1000"
    print "Please guess a number."
    print "You have %s guesses remaining." %count_limit
        
def input_guess(guess):
    # main game logic goes here	
    global secret_number
    global count_limit
    global game    
    guess = int(guess)
    count_limit -= 1 
    print " "
    print "Your guess was %s." %guess
    if secret_number > guess :
        print "Higher!"
        print "You have %s guesses remaining." %count_limit
    elif secret_number < guess :
        print "Lower!"
        print "You have %s guesses remaining." %count_limit
    else:
        print "Correct!"
        if game:
            range100()
        else:
            range1000()
    if count_limit <= 0 :
        print "You lose, sorry."
        if game:
            range100()
        else:
            range1000()
            

# create frame
f = simplegui.create_frame("Guess the Number", 200, 200)
## Window elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game 
range100()
f.start()
