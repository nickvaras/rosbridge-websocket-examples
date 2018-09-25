from json import dumps, loads
# 'pip install ws4py' or 'sudo apt-get install python-ws4py' .See: https://ws4py.readthedocs.io/en/latest/sources/install/
from ws4py.client.threadedclient import WebSocketClient
from math import sin, cos
from time import sleep


class MyRosbridgeClient(WebSocketClient):

    def opened(self):
        print "Connection opened..."

    def advertise_topic(self):
        msg = {'op': 'advertise', 'topic': '/move_base_simple/goal',
            'type': 'geometry_msgs/PoseStamped'}
        self.send(dumps(msg))

    def closed(self, code, reason=None):
        print code, reason

    def move_to(self, x, y, z, w):
        msg = {'op': 'publish',
        'topic': '/move_base_navi_simple/goal',
        'msg':
        {
        'header': {'frame_id': 'map'},
        'pose': {"position": {'x': x, 'y': y}, 'orientation': {'z': z, 'w': w}}
        }}
        self.send(dumps(msg))

    def go_to_named_waypoint(self,waypoint_name):
        msg = { "op": "call_service",
        "service": '/waypoint_db/retrieve_waypoint',
        "args": 
        {
        "mapName":'WebGen',
        "waypointName":waypoint_name
        }}
        self.send(dumps(msg))
    
    def received_message(self, m):
        print m
        waypoint_coordinates  = loads(str(m))
        x_coordinate = waypoint_coordinates['values']['response']['x']
        y_coordinate = waypoint_coordinates['values']['response']['y']
        z_coordinate = waypoint_coordinates['values']['response']['z']
        w_coordinate = waypoint_coordinates['values']['response']['w']
        self.move_to(x_coordinate,y_coordinate,z_coordinate,w_coordinate)


if __name__=="__main__":
    try:
        my_websocket_client = MyRosbridgeClient('ws://35.188.228.188:9090/')
        my_websocket_client.connect()
        my_websocket_client.advertise_topic()              
        my_websocket_client.go_to_named_waypoint('Start')
        sleep(2)  
        # my_websocket_client.run_forever()
    except KeyboardInterrupt:
        my_websocket_client.close()
