Python Robotics Simulator
================================

Python application developed that at the University of Genoa in the academic year 2022/2023 during the Research Track I course, the aim of the project is to solve the concurrency problem for a mobile holonomic robot that matches boxes in a simulator developed by [Student Robotics](https://studentrobotics.org) 

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Once the dependencies are installed, to run the script in the simulator
it is enough to pass the name of the script to run.py, for example:
``` bash
$ python2 run.py script_name.py
```

Robot API
---------
The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].
### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/

## Assignment
The task to be achieved in the simulated robotic enviroment is to pair silver boxes
to golden boxes placed along the border of a square.

### Pseudo code ###
while list of golden boxes paired not full
	if flag token equal to silver:
		look for box with silver flag and silver list
	else:
		look for token with gold flag and gold list
	if distance obtained when searching equal to -1:
		token not in the robot's vision, turn to change the field view
	else if distance less than the threshold :
		grab the box, rotate left to set a clockwise direction to pair 
		boxes and add its code to the silver list 
	else if distance less than the threshold and the dimension of the box and flag set to gold:
		we are carrying a silver box and we are close to golden box, 
		release silver box and add the code of the golden one to the list, 
		then go back to not be too close to the new pair and rotate right
		to set a clockwise direction to pair boxes and counterbalance the
		rotation made to reach and grab the silver box
	else if the robot is well aligned to the token:
		drive towards the token
	else if the robot is not well aligned to the token:
		turn left or right based on the needed rotation
End, task achieved!

### Possible improvements ###
A possible adjustment could be to improve the robot's vision, in order to enlarge the field view
and avoid turning multiple times when the token are close to the robot.
If the boxes in the enviroment were not supposed to be well displaced like in the analyzed scenario, a more sophisticated 
algortihm could have been implemented in order to avoid collisions with boxes along the path of the robot; in this 
case a simpler approach was preferred so as to achieve the task in the easiest way.
	
		
		
	


