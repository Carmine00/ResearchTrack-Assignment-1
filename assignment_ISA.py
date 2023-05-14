from __future__ import print_function

import time
import math
import os
from sr.robot import *

start = time.time()

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""


R = Robot()
token_to_find = "silver"
""" string: Indicstion of which box should the robot look for first"""

ordered_boxes=[]
""" list: list of boxes used by the robot"""

direction = 1
code_to_find = 0   
finished = False


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_token(color, code):
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    code (float): id number of the token (-1 if no token is detected)
    """
    if(color == "silver"):
        m = MARKER_TOKEN_SILVER
    elif(color == "gold"):
        m = MARKER_TOKEN_GOLD

    dist = 100
    for token in R.see():
        if(code == 0):
            if token.dist < dist and token.info.marker_type == m and (token.info.code, token.info.marker_type) not in ordered_boxes:
                dist = token.dist
                return_code = token.info.code
                rot_y = token.rot_y

        else:
            if token.dist < dist and token.info.marker_type == m and (token.info.code, token.info.marker_type) not in ordered_boxes and code == token.info.code:
                dist = token.dist
                return_code = token.info.code
                rot_y = token.rot_y

    if(dist == 100):
	    return -1, -1, -1
    else:
   	    return dist, rot_y, return_code


def find_closest_gold():
    """
    Function to find the closest golden token among all. 
    - If the robot find a token closest than the prevoius one and the next one (due to the distribution of the world), it returns that token because is the closest among all
    - If the robot has seen all the tokens, it returns understanding that the last token is the closest.

    Returns:
	final_code (float): id number of the token (-1 if no token is detected)
    """
    arr_gold = []
    codes = []
    not_all = True

    c = 0
    for cod,col in ordered_boxes:
        if(col == 'gold-token'):
            c += 1

    tokens_seen = 0
    while(not_all):
        dist, rot_y, code = find_token("gold", 0)

        if(len(arr_gold) >= 2 and dist > arr_gold[-1][0] and arr_gold[-1][0] < arr_gold[-2][0] and code != arr_gold[-1][1]):
            not_all = False

        elif(tokens_seen + c == 5):
            not_all = False

        elif(dist != -1 and code not in codes):
            arr_gold.append((dist, code))
            codes.append(code)
            tokens_seen += 1

        turn(20, 0.1)
        print("Looking closest gold token...")

    min_dist = 100
    final_code = 0
    for dist, code in arr_gold:
        if(dist < min_dist):
            min_dist = dist
            final_code = code

    print("Closest gold token: ", final_code)
    return final_code


def get_rotation_vel(rot_y):
    """
    Function that calculates the robot rotation velocity proportional to the angle

    Returns:
	turn_vel (float): velocity of turning
    """
    turn_vel = math.exp(0.3*abs(rot_y)) # Proportional velocity to the angle
    if(turn_vel > 15): # Stablish a limit
        turn_vel = 15
    if(turn_vel <= 0): # Stablish a limit
        turn_vel = 0.1

    return turn_vel
 

def get_velocity(dist):
    """
    Function that calculates the robot linear velocity proportional to the distance

    Returns:
	velocity (float): linear velocity
    """
    if(dist <= 0.7):
        velocity = 10
    else:
        velocity = dist*100 #Proportional velocity to the distance

    if(velocity > 300): # Stablish a limit
        velocity = 300

    if(velocity <= 0):  # Stablish a limit
        velocity = 10

    return velocity


while(not finished):
    if(len(ordered_boxes) == 10):
        finished = True
    
    dist, rot_y, code = find_token(token_to_find, code_to_find)
    print("Distance: ", dist, " Angle: ", rot_y, " Code: ", code)

    if(dist == -1 or rot_y == -1):
        print("Turning...")
        turn(direction*20, 0.1)
    
    elif(dist <= d_th):
        print("Got it!")

        if(token_to_find == "gold"):
            R.release()
            print("Silver token released!")
            token_to_find = "silver"
            d_th = 0.4
            drive(-30, 1)
            ordered_boxes.append((code, MARKER_TOKEN_GOLD))
            code_to_find = 0
            direction = 1

        else:
            R.grab()
            print("Silver token grabbed!")
            token_to_find = "gold"
            d_th = 0.6
            ordered_boxes.append((code, MARKER_TOKEN_SILVER))
            code_to_find = find_closest_gold()
            direction = -1
            
    elif(rot_y <= a_th and rot_y >= -a_th):
        print("Centered! Going forward...")
        velocity = get_velocity(dist)
        drive(velocity,0.1)

    elif(rot_y > a_th):
        print("Turning to the right...")
        turn_vel = get_rotation_vel(rot_y)
        turn(1*turn_vel, 0.1)

    elif(rot_y < -a_th):
        print("Turning to the left...")
        turn_vel = get_rotation_vel(rot_y)
        turn(-1*turn_vel, 0.1)

print("FINISHED")
end = time.time()
print("Task achieved! Time elapsed: "+ str(end - start))
exit()
