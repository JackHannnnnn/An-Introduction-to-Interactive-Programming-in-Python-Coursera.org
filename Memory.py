# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 17:08:48 2016

@author: Chaofan
"""

# implementation of card game - Memory

import simplegui
import random

cards_index = range(0,16)

# helper function to initialize globals
def new_game():
    global cards_list,state,counter,exposed
    cards_list = range(0,8) + range(0,8)
    random.shuffle(cards_list)
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    state = 0
    counter = 0
    label.set_text('Turns = ' + str(counter))
         
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state,a,b,counter
    # a and b stand for the index of the 1st and 2nd exposed card separately
    x = pos[0]
    if state == 0:
        for i in cards_index:
            if exposed[i] == True:
                pass
            elif i*50 <= x < (i+1)*50:
                exposed[i] = True
                a = i
                counter += 1
        state = 1
    elif state == 1:
        for i in cards_index:
            if exposed[i] == True:
                pass
            elif i*50 <= x < (i+1)*50:
                exposed[i] = True
                b = i
        state = 2
    else:
        if cards_list[a] != cards_list[b]:
            exposed[a] = False
            exposed[b] = False
        for i in cards_index:
            if exposed[i] == True:
                pass
            elif i*50 <= x < (i+1)*50:
                exposed[i] = True
                a = i    
                counter += 1
        state = 1
    label.set_text('Turns = ' + str(counter))
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in cards_index:
        if exposed[i] == True:
            canvas.draw_text(str(cards_list[i]),(10+50*i,70),50,'white')
        elif exposed[i] == False:
            canvas.draw_polygon([(0+50*i,0),(50+50*i,0),(50+50*i,100),(0+50*i,100)],1,'black','green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

