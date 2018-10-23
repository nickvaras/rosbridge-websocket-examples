from robot_driver import MyRosbridgeClient
from time import sleep

try:
    my_websocket_client = MyRosbridgeClient('ws://35.188.228.188:9090/')
    my_websocket_client.connect()
    #my_websocket_client.advertise_topic()              
    #my_websocket_client.go_to_named_waypoint('Start')
    my_websocket_client.start_mission('start_nayan_x_3')
    sleep(2)  
    # my_websocket_client.run_forever()
except KeyboardInterrupt:
    my_websocket_client.close()
