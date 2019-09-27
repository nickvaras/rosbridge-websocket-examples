const WebSocket = require('ws');   // sudo npm i ws

var RobotDriver = function(){
    that = this;
    this.ws = new WebSocket('ws://35.199.36.232:9090');    
    this.robotLocation = {x: null, y: null};    

    this.ws.on('open', function open() {
        console.log('New connection');   
         
    });

    this.ws.on('message', function(msg){
        console.log(msg);
        let received_message  = JSON.parse(msg);
        switch(received_message.op){
            case 'service_response':
                switch(received_message.service){
                    case '/mission_control/stop_mission_file':
                        console.log('Mission Stopped');
                        break;
                    case '/waypoint_db/retrieve_waypoint':
                        that.publishGoal(msg);
                }
                break;
            case 'publish':
                this.ws.robotLocation.y = received_message.msg.position.y;
                this.ws.robotLocation.x = received_message.msg.position.x;
                Console.log('Coordinates received. console.log(ws.robotLocation):')
                Console.log(ws.robotLocation);
                this.ws.queryPosition(false);
        }
    });
    
    this.ws.on('close', function() {
        console.log('closing connection');
        this.ws.close();
    });

}

RobotDriver.prototype.goToWaypoint = function(waypointName){
    let request_coordinates_msg ={"op":"call_service","service":"/waypoint_db/retrieve_waypoint","args":{"waypointName": waypointName}};
    this.ws.send(JSON.stringify(request_coordinates_msg));
}



RobotDriver.prototype.runMission = function(missionName){
    let request_mission_msg ={"op":"call_service","service":"/mission_control/run_mission_from_file","args":{"request":missionName}};
    this.ws.send(JSON.stringify(request_mission_msg));
};



RobotDriver.prototype.publishGoal = function(msg){
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
    this.ws.send(JSON.stringify(pose_message));
}

RobotDriver.prototype.cancelGoal = function(){
    console.log('trying to cancel goal');
    let pose_message =  {"op": "publish",
    "topic": "/move_base_navi/cancel",
    "msg":{ "stamp": "",
            "id": ""}
    }; 
    this.ws.send(JSON.stringify(pose_message));
}

RobotDriver.prototype.stopLoop = function(){
    let stopLoopMsg ={"op":"call_service","service":"/mission_control/stop_mission_file","args":{"request":""}};
    this.ws.send(JSON.stringify(stopLoopMsg));
};

RobotDriver.prototype.queryPosition = function(onOff){
    let op = "subscribe";
    if(onOff===false){
        op="unsubscribe";
    }
    let pose_subscribe_message =  {"op": op,
        "topic": "/robot_pose",
        };  
    this.ws.send(JSON.stringify(pose_subscribe_message));
}

module.exports = new RobotDriver();
