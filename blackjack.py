# Mini-project #6 - Blackjack
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com  
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")      

# initialize some useful global variables
in_play = False
score = 0
outcome = "Whaddaya say, pal? You wanna hit, or stand?"
announce = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
    def drawBack(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0] + 1, pos[1] + CARD_BACK_CENTER[1] + 1], CARD_BACK_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        my_string = ""
        for card in self.hand:
            my_string = my_string + str(card) + " "
        return "Looks like ya got " + my_string.strip()

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        value = 0 # if "A" == 1
        sum_aces = 0 # counter for Aces
        for card in self.hand:
            rank = card.get_rank()
            value += VALUES.get(rank)
            if rank == "A":
                sum_aces += 1
        ten_point = value + (10 * sum_aces) - sum_aces  # change Aces to "A" == 10
        if ten_point <= 21:
            value = ten_point
        return value
   
    def draw(self, canvas, pos):
        for card in self.hand:
            pos[0] = pos[0] + CARD_SIZE[0] + 20
            card.draw(canvas, pos)
        
# define deck class 
class Deck:
    def __init__(self):
        self.hand = []
        for suit in SUITS:
            for rank in RANKS:
                self.hand.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.hand)

    def deal_card(self):
        return self.hand.pop()
    
    def __str__(self):
        my_string = ""
        for card in self.cards:
            my_string = my_string + str(card) + " "
        return "Looks like the deck's got " + my_string.strip()

#define event handlers for buttons
def deal():
    global in_play, outcome, announce, score, deck, player, dealer 
    if in_play:
        score -= 1
        in_play = False
        deal()
    else:    
        player = Hand()
        dealer = Hand()
        deck = Deck()
        deck.shuffle()
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        outcome = "Hit or Stand?"
        announce = "Well, what'll it be, Mac?"
        in_play = True

def hit():
    global in_play, outcome, announce, score, deck, player, dealer
    if in_play:
        if player.get_value() < 22:
            player.add_card(deck.deal_card())
            if player.get_value() > 21:
                announce = "Looks like you gone and busted!"
                score -= 1
                outcome = "Whaddaya say? Want me to deal another hand?"
                in_play = False
       
def stand():
    global in_play, outcome, announce, score, deck, player, dealer
    if in_play:
        while (dealer.get_value() < 17):
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            announce = "Dealer busts!"
            outcome = "Want me to deal again, there, buddy?"
            score += 1
            in_play = False
        elif player.get_value() > dealer.get_value():
            announce = "Well, looky there! Player wins!"
            outcome = "Whaddaya say, Mac? Want me to deal another hand?"
            score += 1
            in_play = False
        else:
            announce = "Dealer wins! Better luck next time, Mac."
            outcome = "Shall I deal again, or you ready to call it quits?"
            score -= 1
            in_play = False

# draw handler    
def draw(canvas):
    canvas.draw_text("BLACKJACK", (200, 100), 90, "Red")
    canvas.draw_text("Jimmy,", (78, 150), 32, "Black")
    canvas.draw_text("the Dealer", (62, 187), 32, "Black")
    canvas.draw_text("You, my friend,", (22, 350), 32, "Black")
    canvas.draw_text("the Player", (62, 387), 32, "Black")
    canvas.draw_text(outcome, (300, 200), 30, "White")
    canvas.draw_text(announce, (300, 157), 30, "White")
    canvas.draw_text("Score = " + str(score), (420, 500), 22, "Black")
    dealer.draw(canvas, [-57, 200])
    player.draw(canvas, [-57, 400])
    if in_play:
        dealer.hand[0].drawBack(canvas, [27, 200])
        
# initialization frame
frame = simplegui.create_frame("Blackjack", 1000, 580)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
deal()
