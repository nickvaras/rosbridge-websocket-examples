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

     def move_to(self, x,y,theta):
          msg = {'op': 'publish',
          'topic': '/move_base_simple/goal',
          'msg':
          {
          'header':{'frame_id':'map'} ,
          'pose':{"position" : {'x': x , 'y':y }, 'orientation' : {'z': sin(theta/2.0) , 'w': cos(theta/2.0) } }
          }}
          self.send(dumps(msg))

if __name__=="__main__":
     try:
         ws = MyRosbridgeClient('ws://127.0.0.1:9090/')
         ws.connect()
         ws.advertise_topic()
         ws.move_to(0,0,90)
     except KeyboardInterrupt:
         ws.close()
