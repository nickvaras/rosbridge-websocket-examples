const WebSocket = require('ws');   // sudo npm i ws
const ws = new WebSocket('ws://35.188.228.188:9090');

ws.robotLocation = {x: null, y: null};

ws.on('open', function open() {
    console.log('New connection');    
});

ws.goToWaypoint = function(waypointName){
    let request_coordinates_msg ={"op":"call_service","service":"/waypoint_db/retrieve_waypoint","args":{"mapName":"WebGen","waypointName": waypointName}};
    ws.send(JSON.stringify(request_coordinates_msg));
};

ws.on('message', function(msg){
    console.log(msg);
    let received_message  = JSON.parse(msg);
    switch(received_message.op){
        case 'service_response':
            switch(received_message.service){
                case '/mission_control/stop_mission_file':
                    console.log('Mission Stopped');
                    break;
                case '/waypoint_db/retrieve_waypoint':
                    ws.publishGoal(msg);
            }
            break;
        case 'publish':
            ws.robotLocation.y = received_message.msg.position.y;
            ws.robotLocation.x = received_message.msg.position.x;
            Console.log('Coordinates received. console.log(ws.robotLocation):')
            Console.log(ws.robotLocation);
            ws.queryPosition(false);
    }
});

ws.on('close', function() {
    console.log('closing connection');
    ws.close();
});

ws.publishGoal = function(msg){
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
}

ws.cancelGoal = function(){
    console.log('trying to cancel goal');
    let pose_message =  {"op": "publish",
    "topic": "/move_base_navi/cancel",
    "msg":{ "stamp": "",
            "id": ""}
    }; 
    ws.send(JSON.stringify(pose_message));
}

ws.stopLoop = function(){
    let stopLoopMsg ={"op":"call_service","service":"/mission_control/stop_mission_file","args":{"request":""}};
    ws.send(JSON.stringify(stopLoopMsg));
};

ws.queryPosition = function(onOff){
    let op = "subscribe";
    if(onOff===false){
        op="unsubscribe";
    }
    let pose_subscribe_message =  {"op": op,
        "topic": "/robot_pose",
        };  
    ws.send(JSON.stringify(pose_subscribe_message));
}

module.exports = ws;
