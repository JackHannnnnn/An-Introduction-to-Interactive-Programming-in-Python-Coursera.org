# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 17:05:30 2016

@author: Chaofan
"""

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

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
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        s = ""
        for i in self.cards:
            s += ' ' + str(i)
        return 'Hand contains' + s

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        cards_rank = ''
        hand_value = 0
        for i in self.cards:
            cards_rank += i.get_rank()
            hand_value += VALUES[i.get_rank()]
        if 'A' not in cards_rank:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        d = 0
        for i in self.cards:
            i.draw(canvas,(pos[0] + 96*d, pos[1]))  
            d += 1

        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i,j))

    def shuffle(self):
        random.shuffle(self.deck) 

    def deal_card(self):
        a = random.choice(self.deck)
        self.deck.remove(a)
        return a
    
    def __str__(self):
        s = ""
        for i in self.deck:
            s += ' ' + str(i)
        return 'Deck contains' + s

#define event handlers for buttons
def deal():
    global prompt,outcome,in_play,new_deck,new_player,new_dealer
    prompt = 'Hit or stand?'
    outcome = ''   
    in_play = True
    new_deck = Deck()
    new_deck.shuffle()
    new_player = Hand()
    new_dealer = Hand()
    for i in range(2):
        new_player.add_card(new_deck.deal_card())
        new_dealer.add_card(new_deck.deal_card())

def hit():
    global in_play,outcome,score,prompt
    if in_play == True:
        if new_player.get_value() <= 21:
            new_player.add_card(new_deck.deal_card())
            if new_player.get_value() >21:
                outcome = 'You went bust and lose.'
                prompt = 'New deal?'
                score -= 1
                in_play = False
   
       
def stand():
    global in_play,outcome,score,prompt
    if in_play == True:
            while new_dealer.get_value() < 17:
                new_dealer.add_card(new_deck.deal_card())
            in_play = False
            if new_dealer.get_value() > 21:
                outcome = 'Dealer went bust and you win.'
                prompt = 'New deal?'
                score += 1
            else:
                if new_player.get_value() > new_dealer.get_value():
                    outcome = 'You win.'
                    prompt = 'New deal?'
                    score += 1
                else:
                    new_player.get_value() <= new_dealer.get_value()
                    outcome = 'You lose.'
                    prompt = 'New deal?'
                    score -= 1           
    

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    new_dealer.draw(canvas,(100,200))
    new_player.draw(canvas,(100,400))
    canvas.draw_text('Blackjack',(150,100),40,'Aqua','sans-serif')
    canvas.draw_text('Dealer',(100,170),30,'black')
    canvas.draw_text('Player',(100,370),30,'black')
    canvas.draw_text('Score ' + str(score),(400,100),30,'black')
    canvas.draw_text(prompt,(250,370),30,'black')
    canvas.draw_text(outcome,(250,170),30,'black')
    if in_play == True:
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,[100+CARD_BACK_CENTER[0],200+CARD_BACK_CENTER[1]],CARD_BACK_SIZE)
    else:
        new_dealer.draw(canvas,(100,200))


# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()

