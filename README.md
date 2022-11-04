Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, to run one or more scripts in the simulator, 
use `run.py`, passing it the file names. 

## Problem
The problem to be solved in the simulated robotic enviroment is to pair silver boxes
to golden boxes placed along the border of a square.

### Pseudo code ###
while list of golden boxes paired not full
	if flag token equal to silver:
		look for box with silver flag and silver list
	else:
		look for token with gold flag and gold list
	if distance obtained when searching equat to -1:
		token not in the robot's vision, rotate to change the field view
	else if distance less than a threshold :
		grab the box and add its code to the silver list 
		(DA SPIEGARE perchè siamo nel caso silver)
	else if distance less than a threshold plus the dimension of the box
		we are close to golden box, release silver box and add
		the code of the golden one to the list, then go back to not
		be too close to the new pair and rotate right
	else if the robot is well aligned to the token
		drive towards the token
	else if the robot is not well aligned to the token
		turn left or right based on the necessary rotation
end, task achieved!
	
		
		
	


