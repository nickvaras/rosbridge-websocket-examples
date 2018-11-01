from json import dumps, loads
# 'pip install ws4py' or 'sudo apt-get install python-ws4py' .See: https://ws4py.readthedocs.io/en/latest/sources/install/
from ws4py.client.threadedclient import WebSocketClient
from math import sin, cos
from time import sleep


class MyRosbridgeClient(WebSocketClient):

    def __init__(self, address_port):
        WebSocketClient.__init__(self, address_port)
        self.robot_position_x = None
        self.robot_position_y = None
        self.waypoint_coordinates_x = None
        self.waypoint_coordinates_y = None
        self.coordinates_message_received = False
        self.move_to_waypoint_when_coordinates_received = False
        self.navigation_finished = False
        self.navigation_succeeded = False

    def opened(self):
        print "Connection opened..."
        self.subscribe_to_robot_pose()

    def advertise_topic(self):
        msg = {'op': 'advertise', 'topic': '/move_base_simple/goal',
               'type': 'geometry_msgs/PoseStamped'}
        self.send(dumps(msg))

    def closed(self, code, reason=None):
        print code, reason

    def move_to(self, x, y, z, w):
        self.navigation_finished = False
        self.navigation_succeeded = False
        msg = {'op': 'publish',
               'topic': '/move_base_navi_simple/goal',
               'msg':
               {
                   'header': {'frame_id': 'map'},
                   'pose': {"position": {'x': x, 'y': y}, 'orientation': {'z': z, 'w': w}}
               }}
        self.send(dumps(msg))

    def go_to_named_waypoint(self, waypoint_name):
        self.move_to_waypoint_when_coordinates_received = True
        self.request_waypoint_coordinates(waypoint_name)

    def cancel_goal(self):
        msg = {"op": "publish",
               "topic": '/move_base_navi/cancel',
               "msg":
               {
                   "stamp": "",
                   "id": ""}}
        self.send(dumps(msg))

    def received_message(self, msg):
        #print msg
        message = loads(str(msg))
        if message['op'] == 'service_response':
            if message['service'] == '/mission_control/stop_mission_file':
                print('Mission Stopped')
            elif message['service'] == '/waypoint_db/retrieve_waypoint':
                x_coordinate = message['values']['response']['x']
                y_coordinate = message['values']['response']['y']
                z_coordinate = message['values']['response']['z']
                w_coordinate = message['values']['response']['w']
                self.waypoint_coordinates_x = x_coordinate
                self.waypoint_coordinates_y = y_coordinate
                self.coordinates_message_received = True                
                if self.move_to_waypoint_when_coordinates_received:
                    self.move_to_waypoint_when_coordinates_received = False
                    self.move_to(x_coordinate, y_coordinate, z_coordinate, w_coordinate)

        elif message['op'] == 'publish':
            if message['topic'] == "/move_base_navi/result":
                self.navigation_finished = True
                if message['msg']['status']['text'] == "Goal reached.":
                    self.navigation_succeeded = True
                
            else:
                # update the robot position
                self.robot_position_x = message['msg']['position']['x']
                self.robot_position_y = message['msg']['position']['y']

    def start_mission(self, mission_name):
        msg = {"op": "call_service",
               "service": "/mission_control/run_mission_from_file",
               "args": {"request": mission_name}}
        self.send(dumps(msg))

    def stop_mission(self):
        msg = {"op": "call_service",
               "service": "/mission_control/stop_mission_file",
               "args": {"request": ""}}
        self.send(dumps(msg))

    def subscribe_to_robot_pose(self):
        msg = {"op": "subscribe", "topic": "/robot_pose"}
        self.send(dumps(msg))

    def subscribe_to_navigation_result(self):
        msg = {"op": "subscribe", "topic": "/move_base_navi/result"}
        self.send(dumps(msg))

    def request_waypoint_coordinates(self, waypoint_name):
        msg = {"op": "call_service",
               "service": '/waypoint_db/retrieve_waypoint',
               "args":
               {
                   "mapName": 'WebGen',
                   "waypointName": waypoint_name
               }}
        self.send(dumps(msg))

    def get_waypoint_coordinates(self, waypoint_name):
        self.request_waypoint_coordinates(waypoint_name)
        while not self.coordinates_message_received:
            sleep(0.15)
        self.coordinates_message_received = False
        return self.waypoint_coordinates_x, self.waypoint_coordinates_y
        
