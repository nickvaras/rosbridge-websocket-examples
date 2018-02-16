from json import dumps
from ws4py.client.threadedclient import WebSocketClient   # 'pip install ws4py' or see: https://ws4py.readthedocs.io/en/latest/sources/install/
from math import sin, cos

class MyRosbridgeClient(WebSocketClient):

     def opened(self):
         print "Connection opened..."

     def advertise_topic(self):
         msg = {'op': 'advertise','topic': '/move_base_simple/goal','type': 'geometry_msgs/PoseStamped'}
         self.send(dumps(msg))

     def closed(self, code, reason=None):
         print code, reason

     def move_to(self, coords):
          x = coords[0]
          y = coords[1]
          theta = coords[2]
          msg = {'op': 'publish',
          'topic': '/move_base_simple/goal',
          'msg':
          {
          'header':{'frame_id':'map'} ,
          'pose':{"position" : {'x': x , 'y':y }, 'orientation' : {'z': sin(theta/2.0) , 'w': cos(theta/2.0) } }
          }}
          self.send(dumps(msg))

class Basic2DTransformer(object):

     def __init__(self,dx,dy,dtheta):
         self.delta_x =  dx
         self.delta_y =   dy
         self.delta_theta = dtheta

     def transform_target_from_external_frame_to_robot_frame(self, x, y, theta):
         x_robot = x * cos(self.delta_theta) + y * sin(self.delta_theta) - self.delta_x
         y_robot = -x * sin(self.delta_theta) + y * cos(self.delta_theta) - self.delta_y
         theta_robot = theta - self.delta_theta

         return x_robot, y_robot , theta_robot

if __name__=="__main__":
     try:
         ws = MyRosbridgeClient('ws://127.0.0.1:9090/')
         ws.connect()
         ws.advertise_topic()
         """ Next we establish the correspondence (or shift) between an existing 
             coordinate frame and the robot's map frame. Note that ROS has a superb transforms module, but this example is
             made so it is 100% off-ROS. The assumptions in this case are that both coordinate frames are 2D and in the same plane, and that both are XY 
             right-hand rule frames, i.e., a z axis would point towards the onlooker. 
             Also, it is assumed that both frames express coordinates in meters and radians.
             IMPORTANT: that delta_x is the distance along the robot frame x axis, going from the origin of the preexisting frame back to the origin of the robot frame.
             Similarly, delta_y is the distance along the y axis of the robot frame, tha goes from the origin of the preexisting frame to the origin of 
             the origin of the robot frame. delta_theta in this case (again, expressed in radians) is the rotation between frames from the preexisting frame to the
             robot frame. Make sure you check and test these correspondence and get them right before sending targets to the robot.
	 """

	 # shift values are set to zero, which is equivalent to say that we are setting goals in the robot frame
         transformer = Basic2DTransformer(0.0,0.0,0.0)

         target_coordinates= transformer.transform_target_from_external_frame_to_robot_frame(4.23,1.54,0.0)  
         print(target_coordinates)
	 #send the coordinates to the robot
         ws.move_to(target_coordinates)  
     except KeyboardInterrupt:
         ws.close()
