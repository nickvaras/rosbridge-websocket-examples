# rosbridge-python-websocket-example
A bare-bones example to send a command to a robot using rosbridge over websockets, tested on Python 2.7

Rosbridge enables virtually any device to interact with a ROS system.
This example focuses in a ROS robot with enabled websockets rosbridge, such as Vector by Waypoint Robotics (http://waypointrobotics.com).

This example has been deliberately simplified to the bare-minimum code needed to send a command to a robot to go to a set of coordinates on a map, and optionally, by setting the transform values between frames, a target to a robot can be expressed in a preexisting coordinate frame (this example intends to show how any non-ROS device can interact with a ROS system, hence the superb tf ROS module is not used)

Other than Python, it only requires the ws4py websocket library to be installed:
pip install ws4py' or see: https://ws4py.readthedocs.io/en/latest/sources/install/

Inspired by
https://github.com/Sanic/ROSBridgeTestclient 
and this answer:
https://answers.ros.org/question/40020/thin-clients-communicating-with-ros/
