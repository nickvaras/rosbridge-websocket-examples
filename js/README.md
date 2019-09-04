# rosbridge-javascript-websocket-example

An example on how to use the robot-driver example:

Import it into your current script or in interactive mode:

``const myws = require('./robot-driver')``

This will establish the connection with the server and make the  example's methods available.

To query the robot's current location you'd do:

``myws.queryPosition()``

...which will store the coordinates in the robotLocation attribute for further use. For example:

``console.log(myws.robotLocation)``

To make the robot go to a waypoint:

``myws.goToWaypoint('Start')``


To abort the current goal and stop the robot:

``myws.cancelGoal()``

To run a program created in the Dispatcher User Interface:

``myws.runMission('<the_name_that_I_saved_my_mission_with>)``
