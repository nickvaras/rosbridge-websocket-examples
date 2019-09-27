# JavaScript rosbridge websocket examples

A few examples on how to control a robot over raw javascript websockets.

For script examples, look at go-to-named-waypoint.js or go-to-coordinates.js

For interactive control in the nodejs repl, you can do the following:

``const driver = require('./robot-driver')``

This will establish the connection with the server and make the  example's methods available.

To query the robot's current location you'd do:

``driver.queryPosition()``

...which will store the coordinates in the robotLocation attribute for further use. For example:

``console.log(driver.robotLocation)``

To make the robot go to a waypoint:

``driver.goToWaypoint('Start')``


To abort the current goal and stop the robot:

``driver.cancelGoal()``

To run a program created in the Dispatcher User Interface:

``driver.runMission('<the_name_that_I_saved_my_mission_with>)``
