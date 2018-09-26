const WebSocket = require('ws');   // sudo npm i ws
const ws = new WebSocket('ws://35.188.228.188:9090');

ws.on('open', function open() {
    console.log('New connection');
    let request_coordinates_msg ={"op":"call_service","service":"/waypoint_db/retrieve_waypoint","args":{"mapName":"WebGen","waypointName": "Start"}};
    ws.send(JSON.stringify(request_coordinates_msg));
});

ws.on('message', function(msg){
    console.log(msg);
    waypoint_coordinates  = JSON.parse(msg);
    x_coordinate = waypoint_coordinates.values.response.x;
    y_coordinate = waypoint_coordinates.values.response.y;
    z_coordinate = waypoint_coordinates.values.response.z;
    w_coordinate = waypoint_coordinates.values.response.w;
    let pose_message =  {"op": "publish",
                        "topic": "/move_base_navi_simple/goal",
                        "msg":{ "header": {"frame_id": "map"},
                            "pose": {"position": {"x": x_coordinate, "y": y_coordinate}, "orientation": {"z": z_coordinate, "w": w_coordinate}}}
                        }; 
    ws.send(JSON.stringify(pose_message));
});

ws.on('close', function() {
    console.log('closing connection');
    ws.close();
});