

ws = null;
shock = 0;
shockRec = 0;
function create_ws() {


  // Let us open a web socket
  var ws_url = $("#el_ws_url").val();
    shock = 0;
    shockRec = 0;
  ws = new WebSocket(ws_url);
  alert("WebSocket created");

  ws.onopen = function() {
    alert("WS opened");
    $("#ws_online").show();
    $("#ws_offline").hide();
  };

  ws.onmessage = function (evt) {
    var received_msg = evt.data;
    console.log(received_msg);
  };

  ws.onclose = function() {
    ws = null;
    $("#ws_online").hide();
    $("#ws_offline").show();
  };

  setInterval(ws_send_gamepad, 500);
}



function ws_send_gamepad() {
    var ws_url = $("#el_ws_url").val();
    const Http = new XMLHttpRequest();
    const url = "http://"+ws_url.substring(5,ws_url.length-5)+":5000/detect";
    Http.open("GET",url);
    Http.send();
    Http.onreadystatechange=(e)=>{
	shockRec = Http.responseText;
    }


    
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
  if (!gamepads) {
    return;
  }

  var gp = gamepads[0];

    if (gp.vibrationActuator && (shockRec!= shock )) {
	gp.vibrationActuator.playEffect("dual-rumble", {

	    duration: 1000,

	    strongMagnitude: 1.0,

	    weakMagnitude: 1.0

	});
	shock = shockRec;
    }



    
  var turn = gp.axes[2];
  var forward = gp.axes[1];

  var pressed = gp.buttons[0];
  if(typeof(pressed)=="object"){
     pressed = pressed.pressed;
  }

  var snap = gp.buttons[1];
  if(typeof(snap)=="object"){
     snap = snap.pressed;
  }

  if(snap){
      console.log("snap");

      var xhr = new XMLHttpRequest();
      var link = "http://"+ws_url.substring(5,ws_url.length-5)+":8080/0/action/snapshot";
      console.log(link);
      xhr.open('GET', link, true);
      xhr.send();
  }
	




  console.log("Cal p: "+pressed);


  console.log(turn);
  console.log(forward);

  if ( !ws ) {
    console.log("no websocket! aborting");
    return;
  }

  ws.send(JSON.stringify({
    turn: turn,
    forward: forward,
    tower: "0",
    pressed:pressed,
    time: Date.now(),
    sid: "{{sessionID}}"
  }));

}


function calibrate() {
    console.log("calibrating");
  if ( !ws ) {
    console.log("no websocket! aborting");
    return;
  }

  ws.send(JSON.stringify({
    turn: 0,
    forward: 0,
    tower: "0",
    pressed:true,
    time: Date.now(),
    sid: "{{sessionID}}"
  }));

}


function disconnect_ws() {
  if ( !ws ) {
    console.log("no websocket! aborting");
    return;
  }
  $("#ws_online").hide();
  $("#ws_offline").show();
  ws.close();
}

$(document).ready(function() {
  if ( !("WebSocket" in window) ) {
    alert("WebSocket NOT supported by your Browser!");
  }
});
