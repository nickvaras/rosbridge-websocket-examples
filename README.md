# rosbridge-python-websocket-example
A bare-bones example to send a command to a robot using rosbridge over websockets, tested on Python 2.7

Rosbridge enables virtually any device to interact with a ROS system.
This example focuses in a ROS robot with enabled websockets rosbridge, such as Vector by Waypoint Robotics (http://waypointrobotics.com).

This example has been deliberately simplified to the bare-minimum code needed to send a command to a robot to go to a set of coordinates on a map.

Based on
https://github.com/Sanic/ROSBridgeTestclient 
and this answer:
https://answers.ros.org/question/40020/thin-clients-communicating-with-ros/

