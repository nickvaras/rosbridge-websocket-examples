from json import dumps, loads
# 'pip install ws4py' or 'sudo apt-get install python-ws4py' .See: https://ws4py.readthedocs.io/en/latest/sources/install/
from ws4py.client.threadedclient import WebSocketClient
from math import sin, cos

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

    def cancel_goal(self):
        msg = { "op": "publish",
        "topic": '/move_base_navi/cancel',
        "msg": 
        {
        "stamp":"",
        "id":""}}
        self.send(dumps(msg))
    
    def received_message(self, msg):
        print msg
        #waypoint_coordinates  = loads(str(msg))
        message  = loads(str(msg))
	if message['op'] == 'service_response':
            if message['service'] == '/mission_control/stop_mission_file':
                print('Mission Stopped')
            elif message['service'] == '/waypoint_db/retrieve_waypoint':
                x_coordinate = message['values']['response']['x']
                y_coordinate = message['values']['response']['y']
                z_coordinate = message['values']['response']['z']
                w_coordinate = message['values']['response']['w']
                self.move_to(x_coordinate,y_coordinate,z_coordinate,w_coordinate)
        elif message['op'] == 'publish':
            pass
	"""
		case 'publish':
		    ws.robotLocation.y = received_message.msg.position.y;
		    ws.robotLocation.x = received_message.msg.position.x;
		    Console.log('Coordinates received. console.log(ws.robotLocation):')
		    Console.log(ws.robotLocation);
		    ws.queryPosition(false);
	    }
	});
	"""
    def start_mission(self,mission_name):
        msg = { "op": "call_service",
        "service": "/mission_control/run_mission_from_file",
        "args": {"request":mission_name }}
        self.send(dumps(msg))

    def stop_mission(self):
        msg = { "op": "call_service",
        "service": "/mission_control/stop_mission_file",
        "args": {"request":"" }}
        self.send(dumps(msg))

