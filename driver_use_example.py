from robot_driver import MyRosbridgeClient
import time

try:
    my_websocket_client = MyRosbridgeClient('ws://35.188.228.188:9090/')
    my_websocket_client.connect()


    # This is an example script, uncomment relevant lines to try different functions

    """ Sending the robot to a waypoint:"""
    my_websocket_client.go_to_named_waypoint('Start')
    
    """ Starting a mission/program"""
    #my_websocket_client.start_mission('start_nayan_x_3')
    

    """ Current approximate robot position can be queried directly like this: """
    #print(my_websocket_client.robot_position_x)
    #print(my_websocket_client.robot_position_y)
    
    """ Use this method to stop any running playlist/mission/program """
    #my_websocket_client.stop_mission()    

    """ Use this method to get the x-y coordinates of a saved waypoint """
    #my_websocket_client.get_waypoint_coordinates('Start')
    
    """ If you want this script to run forever, uncomment this """
    #my_websocket_client.run_forever()
    # or
    time.sleep(5)

except KeyboardInterrupt:
    my_websocket_client.close()
