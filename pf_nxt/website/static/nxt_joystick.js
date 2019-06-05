joystick = null;
ws = null;

function init_joystick() {
  //$("#joystick-container").width($(".div.container").width());
  joystick = new VirtualJoystick({
    container	: document.getElementById('joystick-container'),
    //baseElement	: document.getElementById('joystick-container'),
    //baseElement : document.getElementById('joystick-base'),
    //stickElement : document.getElementById('joystick-container'),
    mouseSupport	: true,
    stationaryBase: true,
    baseX: $("#joystick-container").width() / 2,
    baseY: $("#joystick-container").height() / 2,
    //limitStickTravel : true,
    //stickRadius : $("#joystick-container").height() / 2
  });
  $("#joystick-container").removeClass("bg-secondary");
  $("#joystick-container").addClass("bg-primary");
}

function destroy_joystick() {
  joystick.destroy();
  $("#joystick-container").addClass("bg-secondary");
  $("#joystick-container").removeClass("bg-primary");
}

function create_ws() {

  if ( !joystick ) {
    alert("No joystick found! Aborting.");
    return;
  }

  // Let us open a web socket
  var ws_url = $("#el_ws_url").val();

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

  setInterval(ws_send_joystick, 500);
}

function ws_send_joystick() {

  // normalize joystick values so they are always between -1 and 1
  var turn = 2 * joystick.deltaX() / $("#joystick-container").width();
  var forward = 2 * joystick.deltaY() / $("#joystick-container").height();

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
      pressed:false,  
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
