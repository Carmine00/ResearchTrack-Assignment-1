from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

last_tok = "silver-token"
""" string flag to let the robot know which token has to look for, initialized to silver"""

list_sil = []
""" list related to the codes of the silver tokens found """

list_gold = []
""" list related to the codes of the golden tokens found """

R = Robot()
""" instance of the class Robot"""

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

def find_token(last_tok, list_tok):
    """
    Function to find the closest token
    
    Args: last_tok (string): identifier for the token type: "silver-token" or "gold-token"
          list_tok: list with the codes of the token already found
          
    Returns:
	dist (float): distance of the closest token (-1 if no token is detected) with identifier last_tok and not belonging to list_tok
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	val (int): integer code associated to each token (-1 if no new token is detected)
    """
    dist=100
    for token in R.see():
    	""" 
    	if token is at the minimum distance, it has the specific marker type required and is not part 
    	of the list, then update the new distance, the angle between the robot and the token, and the
    	code associated to it
    	"""
        if token.dist < dist and token.info.marker_type == last_tok and list_tok.count(token.info.code) == 0 :
            dist=token.dist
	    rot_y=token.rot_y
	    val = token.info.code
    if dist==100:
	return -1, -1, -1
    else:
   	return dist, rot_y, val  	  

# while the list of golden tokens paired is not full, keep pairing and searching for boxes 
while len(list_gold)!=6:
    if last_tok == "silver-token": # if last_tok is equal to "silver-token", then we look for a silver token, otherwise for a golden one
	dist, rot_y, val = find_token(last_tok, list_sil)
    else:
	dist, rot_y, val  = find_token(last_tok, list_gold)
    if dist==-1: # if no token is detected, we make the robot turn 
	print("I don't see any token!")
	turn(10, 1)
    elif dist <d_th: 
    	""" 
    	if we are close to the token we have to check two different cases and perform different tasks: 
    	1)we are simply close to the box and therefore we're looking for a silver one and we can grab it, 
    	2) we are close to the token plus a certain length, which takes into account the dimension of a silver box
    	carried by the robot while reaching a gold box, which doesn't need to be grabbed, and the string identifier 
    	for the token is "gold-token"
    	"""
        print("Found it!")
        if R.grab():
		print("Gotcha!")
        	list_sil.append(val) # add code of the last token found to the silver list
	        last_tok = "gold-token"
	        turn(-20,2) 
	else:
		print("Aww, I'm not close enough.")      	
    elif dist <d_th+0.20 and last_tok == "gold-token": 
        list_gold.append(val) # add code of the last token found to the gold list
        R.release()
        drive(-25,2) # go back with respect to the last pair of boxes paired
        turn(20,2) # when pairing we turned left, so to counter balance that rotation we now turn right
        last_tok = "silver-token" 
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	print("Proceeding...")
        drive(30, 0.5)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5) 
# when exiting the while loop, the list of gold token is full and the task has been achieved
print("Task achieved!")
exit()
	
