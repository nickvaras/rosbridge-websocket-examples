# rosbridge-websocket-examples
A set of bare-bones examples mini-drivers to control a mobile robot using rosbridge over websockets.

For a Python example, see python folder.
For Javascript examples, see js folder.

Rosbridge enables virtually any device to interact with a ROS system.
The Rosbridge protocol specification is available [here](https://github.com/RobotWebTools/rosbridge_suite/blob/master/ROSBRIDGE_PROTOCOL.md).

This sample code is meant to demonstrate basic communication without using any special client library, although more sophisticated functionality can be achieved by means of thin client libraries like [roslibjs](http://wiki.ros.org/roslibjs) and [roslibpy](https://github.com/gramaziokohler/roslibpy).

Although the examples were written to interact with a [Waypoint Robotics](http://waypointrobotics.com) Vector robot, they can be adapted to any robot using rosbridge.

Inspired by
https://github.com/Sanic/ROSBridgeTestclient 
and this answer:
https://answers.ros.org/question/40020/thin-clients-communicating-with-ros/

