# rosbridge-python-websocket-example
A set of bare-bones example mini-driver to control a mobile robot using rosbridge over websockets, tested on Python 2.7

Rosbridge enables virtually any device to interact with a ROS system.
This example on a particular ROS robot with enabled websockets rosbridge, Vector by Waypoint Robotics (http://waypointrobotics.com).

See driver_use_example.py for how-to use the driver

``python driver_use_example.py``

Other than Python, it only requires the ws4py websocket library to be installed:
pip install ws4py' or see: https://ws4py.readthedocs.io/en/latest/sources/install/

Inspired by
https://github.com/Sanic/ROSBridgeTestclient 
and this answer:
https://answers.ros.org/question/40020/thin-clients-communicating-with-ros/
