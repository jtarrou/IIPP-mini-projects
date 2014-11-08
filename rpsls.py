## Rules for Rock Paper Scissors Lizard Spock
## Scissors cuts Paper
## Paper covers Rock
## Rock crushes Lizard
## Spock smashes Scissors
## Scissors decapitates Lizard
## Lizard eats Paper
## Paper disproves Spock
## Spock vaporizes Rock
## Rock crushes Scissors (As it always has been)
## 0 - Rock 
## 1 - Spock
## 2 - Paper
## 3 - Lizard
## 4 - Scissors
import random

## helper function, el primero

def name_to_number(name):
    """
    Converts name to number using if/elif/else.
    """
    if name == "rock" :
        return 0
    elif name == "Spock" :
        return 1
    elif name == "paper" :
        return 2
    elif name == "lizard" :
        return 3
    elif name == "scissors" :
        return 4
    # if an invalid choice is made
    else :
        return "No such option."
    print name

## helper function, the second

def number_to_name(number):
    """
    Converts number to name using if/elif/else.
    """
    if number == 0 :
        return "rock"
    elif number == 1 :
        return "Spock"
    elif number == 2 :
        return "paper"
    elif number == 3 :
        return "lizard"
    elif number == 4 :
        return "scissors"
    # if an invalid choice is made
    else :
        return "No such option."
    print number

## main function
def rpsls(player_choice): 
    """
    Takes user input, converts it to number, computes a random number 0:4, then tallies score. 
    Prints result
    """
    
    # print a blank line to separate consecutive games
    
    print " "
    
    # print out the message for the player's choice
    # convert the player's choice to player_number using the function name_to_number()
        
    player_number = name_to_number(player_choice)
    print "Player chooses %s!" %player_choice
    
    # compute random guess for comp_number using random.randrange()
    # convert comp_number to comp_choice using the function number_to_name()
        
    comp_number = random.randrange(0,4)
    comp_name = number_to_name(comp_number)
    print "Computer chooses %s!" %comp_name
    
    # compute difference of comp_number and player_number modulo five
        
    result_rpsls = (comp_number - player_number)%5
        
    # use if/elif/else to determine winner, print winner message
        
    if result_rpsls == 0 :
        print "Player and computer tie!"
    elif result_rpsls == 1 or result_rpsls == 2:
        print "Computer wins!"
        print "Sorry, try again!"
    elif result_rpsls == 3 or result_rpsls == 4 :
            print "Player wins!"
            print "Congratulations! You just cut, covered, crushed, "
            print "smashed, decapitated, ate, vaporized or otherwise "
            print "disapproved of the computer!" 
   
  
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
