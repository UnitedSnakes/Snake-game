# -*- coding: utf-8 -*-
"""
Created on Tue Jan 5 2021

@author: UnitedSnakes
"""

import turtle
import random
import time

def create_writer_turtles():
    """To create invisible turtles
    """
    name = turtle.Turtle()
    name.ht()
    name.up()
    name.speed(0)
    name.width(2)
    return name

def initialize_GUI():
    """To initialize the basic visual frames
    """
    global initializer_turtle, motion_turtle, contact_turtle, time_turtle
    initializer_turtle = create_writer_turtles()

    # Write keywords
    initializer_turtle.goto(-200, 240)
    initializer_turtle.write('Contact:', font = ('Arial', 14, 'normal'))

    initializer_turtle.goto(-30, 240)
    initializer_turtle.write('Time:', font = ('Arial', 14, 'normal')) # + str(time)

    initializer_turtle.goto(103, 240)
    initializer_turtle.write('Motion:', font = ('Arial', 14, 'normal'))

    # Draw margins
    initializer_turtle.goto(-250, 210)
    initializer_turtle.down()
    initializer_turtle.goto(-250, 290)
    initializer_turtle.goto(250, 290)
    initializer_turtle.goto(250, 210)
    initializer_turtle.goto(-250, 210)
    initializer_turtle.goto(-250, -290)
    initializer_turtle.goto(250, -290)
    initializer_turtle.goto(250, 210)
    initializer_turtle.up()

    # Write greetings
    initializer_turtle.goto(-240, 20)
    greetings = """Welcome to Sam\'s snake game!\n\nUse arrow keys to handle the snake.\n
    Try to comsume all the food and avoid head-to-head collision\nwith the monster.Click anywhere to start.\n
    Press the space bar to pause.\n\nMay the force be with you!"""
    initializer_turtle.write(greetings, font = ('Arial', 12, 'normal'))
    
    # Generate three turtles to update the three data coordinately
    motion_turtle = create_writer_turtles()
    motion_turtle.goto(170, 240)
    motion_turtle.goto(0, -40)  # Set a meaningless operation for the first "undo", to be shown in the folowing

    contact_turtle = create_writer_turtles()
    contact_turtle.goto(-120, 240)
    contact_turtle.goto(0, -40)

    time_turtle = create_writer_turtles()
    time_turtle.goto(30, 240)
    time_turtle.goto(0, -40)

def place_food():
    """To place the food numbers without overlapping
    """
    global food_dict, turtlelist
    food_dict = {}
    turtlelist = list(range(1, 10))
    for i in range(1, 10):
        while True:
            food_xcor = random.randrange(-240 - 3, 241 - 3, 20)
            food_ycor = random.randrange(-240 - 8 - 40, 241 - 8 - 40, 20)
            # To align the food with the squares of the snake's body
            if not (food_xcor == 0 - 3 and -40 - 8 <= food_ycor <= -40 + 20*4 - 8) and\
                (food_xcor, food_ycor) not in food_dict:
                # Prevent the food from:
                # 1) being placed at the snake's initial route
                # 2) overlap with each other
                food_dict[(food_xcor, food_ycor)] = str(i)
                break

        turtlelist[i - 1] = create_writer_turtles()
        turtlelist[i - 1].goto(food_xcor, food_ycor)
        turtlelist[i - 1].write(i, font = ('Arial', 12, 'normal'))

def in_square_collision(posA, posB, Length):
    """ To determine if two squares with length 'Length' separately centered at 'PosB' and 'PosA' are in collision.      
    """
    # PosA and PosB must be tuples representing coordinates
    # Length must be a positive number
    if abs(posA[0] - posB[0]) <= Length + 0.0001 and\
        abs(posA[1] - posB[1]) <= Length + 0.0001:
        return True     # 'True' for collision, 'None' for no collision.

def place_monster():
    """To place the monster
    """
    global monster, monster_cor
    monster = turtle.Turtle()
    monster.ht()
    monster.up()
    monster.shape('square')
    monster.color('green')
    monster.speed(0)
    while True:
        monster_cor = (random.randrange(-240 - 3, 241 - 3, 20), random.randrange(-240 - 8 - 40, 241 - 8 - 40, 20))
        if not in_square_collision((monster_cor), (0, -40), 100) and\
            monster_cor not in food_dict:
            # To put it at a relative far place from the snake, and prevent its overlap with the food numbers
            monster.goto(monster_cor)
            monster.st()
            break

def place_snake():
    """To generate the snake and its relative data
    """
    global snake, snake_present_length, snake_theoretical_length, snake_pos_list
    snake = turtle.Turtle()
    snake.speed(0)
    snake.color('yellow', 'orange')
    snake.shape('square')
    snake.shapesize(1, 1, 1.2)
    snake.left(90)
    snake.up()
    snake.goto(0, -40)
    snake_present_length = 1
    snake_theoretical_length = 5
    snake_pos_list = []

def check_food_consumption():
    """To cancel the food number once it was consumed
    """
    global snake_theoretical_length
    for i in food_dict:
        a = (i[0] +3, i[1] + 8)
        if snake.distance(a) <= 0.00001:
            turtlelist[int(food_dict[i]) - 1].undo()
            snake_theoretical_length += int(food_dict[i])
            food_dict.pop(i)
            break

def determine_growing_status():
    """To tell if the snake is lengthening itself
    """
    global growing_flag, snake_present_length, snake_theoretical_length
    if snake_present_length < snake_theoretical_length:
        growing_flag = True     # Return 'True' if the snake is lengthening.
    else:
        growing_flag = False

def snake_growing_move():
    """To advance the snake when it is lengthening itself. 
    """
    global growing_flag, snake_present_length, snake_pos_list
    check_border_collision()
    snake.color('yellow', 'skyblue')
    snake.stamp()
    snake.color('yellow', 'orange')
    snake_pos_list.append(snake.pos())
    snake.fd(20)  # To produce a slower advancement
    snake_present_length += 1

def snake_normal_move():
    """To advance the snake when it is not lengthening itself. 
    """
    check_border_collision()
    snake.color('yellow', 'skyblue')
    snake.stamp()
    snake.color('yellow', 'orange')
    snake_pos_list.append(snake.pos())
    del snake_pos_list[0]
    snake.fd(20)  # To produce a quicker advancement
    snake.clearstamps(1)

def turn_leftwards():
    """To change the direction of the snake.
    """
    global pause_flag
    snake.seth(180)
    if pause_flag == True:      # To cancel the 'Paused' status through arrow keys 
        pause_flag = False

def turn_rightwards():
    global pause_flag
    snake.seth(0)
    if pause_flag == True:
        pause_flag = False

def turn_upwards():
    global pause_flag
    snake.seth(90)
    if pause_flag == True:
        pause_flag = False

def turn_downwards():
    global pause_flag
    snake.seth(270)
    if pause_flag == True:
        pause_flag = False

def change_pause_status():
    """Use a bool variable for the 'paused' or 'non-paused' status
    """
    global pause_flag
    pause_flag = not pause_flag

def bind_keys():
    """Bind physical keys with coordinated functions
    """
    turtle.onkey(turn_leftwards, 'Left')
    turtle.onkey(turn_rightwards, 'Right')
    turtle.onkey(turn_upwards, 'Up')
    turtle.onkey(turn_downwards, 'Down')
    turtle.onkey(change_pause_status, 'space')

def check_border_collision():
    """To check if the snake is going to get rid of the walls
    """
    global border_flag
    if abs(snake.xcor() - (-250 + 10)) <= 0.00000001 and abs(snake.heading() - 180) <= 0.0001 or\
        abs(snake.xcor() - (250 - 10)) <= 0.00000001 and abs(snake.heading() - 0) <= 0.0001 or\
        abs(snake.ycor() - (-250 + 10 - 40)) <= 0.00000001 and abs(snake.heading() - 270) <= 0.0001 or\
        abs(snake.ycor() - (250 - 10 - 40)) <= 0.00000001 and abs(snake.heading() - 90) <= 0.0001:
        border_flag = True
    else:
        border_flag = False

def get_motion_status():
    """To return the status of the snake for the status area
    """
    global motion_status
    if pause_flag == False:
        if snake.heading() == 0:
            motion_status = 'Right'
        if snake.heading() == 90:
            motion_status = 'Up'
        if snake.heading() == 180:
            motion_status = 'Left'
        if snake.heading() == 270:
            motion_status = 'Down'
    else:
        motion_status = 'Paused'

def update_status_area():
    """To update the information in the status area
    """
    global contact, motion_status
    motion_turtle.undo()
    motion_turtle.write(motion_status, font = ('Arial', 14, 'normal'))

    contact_turtle.undo()
    contact_turtle.write(contact, font = ('Arial', 14, 'normal'))

    time_turtle.undo()
    time_turtle.write(int(time.time()) - start_time, font = ('Arial', 14, 'normal'))

    turtle.update()

def monster_move():
    """To advance the monster toward the snake's head
    """
    if 45 < monster.towards(snake) <= 135:
        monster.seth(90)
    elif 135 < monster.towards(snake) <= 225:
        monster.seth(180)
    elif 225 < monster.towards(snake) <= 315:
        monster.seth(270)
    else:
        monster.seth(0)

    multiplier = random.choice((0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1))
    monster.fd(multiplier * 20)     # To make the monster's speed close to the snake's

def detect_termination():
    """To detect if the game should terminate
    """
    global termination_status
    if food_dict == {}:    # If all food had been consumed
        terminator_turtle.goto(snake.pos())
        terminator_turtle.color('blue')
        terminator_turtle.write('Winner!', font = ('Arial', 12, 'normal'))
        termination_status = 'win'

    elif in_square_collision(monster.pos(), snake.pos(), 20):     # If the snake's head was caught by the monster
        terminator_turtle.goto(snake.pos())
        terminator_turtle.color('red')
        terminator_turtle.write('Game Over!', font = ('Arial', 12, 'normal'))
        termination_status = 'lose'

def count_contacts():
    """To check and record if the snake is being contacted by the monster.
    """
    global contact
    for i in snake_pos_list:
        if in_square_collision(monster.pos(), i, 20):
            contact += 1
            break

def main_Loop(x, y):
    """The main process (as a while-loop) for the game.
    """
    global contact, termination_status, terminator_turtle, start_time, food_dict, motion_status

    turtle.onscreenclick(None)      # Unbind the mouse right off, preventing double-click
    turtle.setup(660, 740)
    initializer_turtle.undo()
    turtle.title("Welcome to Sam's snake game!")
    bind_keys()
    place_snake()
    place_food()
    place_monster()
    terminator_turtle = create_writer_turtles()
    start_time = int(time.time())

    while True:
        turtle.listen()
        check_food_consumption()
        determine_growing_status()
        get_motion_status()
        count_contacts()
        update_status_area()
        check_border_collision()
        detect_termination()

        if termination_status != 'None':    # Break the loop and end the game.
            break
        elif pause_flag == False:
            if growing_flag:
                if border_flag:
                    monster_move()
                else:
                    turtle.ontimer(snake_growing_move(), 200)
                    monster_move()
            else:
                if border_flag:
                    monster_move()
                else:
                    snake_normal_move()
                    monster_move()
        else:
            monster_move()
        turtle.update()
        turtle.ontimer(None, 300)
        count_contacts()
        get_motion_status()
        update_status_area()

def main():
    """main function
    """
    global pause_flag, contact, termination_status
    pause_flag = False
    contact = 0
    termination_status = 'None'
    initialize_GUI()
    turtle.onscreenclick(main_Loop)
   
main()
turtle.mainloop()
