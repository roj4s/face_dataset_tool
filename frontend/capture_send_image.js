const SERVER_ENDPOINT = "wss://feis.in:5000/capture";
//const SERVER_ENDPOINT = "wss://localhost:5000/capture";

var ws = new WebSocket(SERVER_ENDPOINT);
var last_instant = new Date().getTime();
var time_threshold = 3;

ws.onmessage = function (evt) {
   console.log("Server said:");
   console.log(evt.data);
};

function dataURLtoBlob(dataURL) {

    var binary = atob(dataURL.split(',')[1]);
    var array = [];
    for(var i = 0; i < binary.length; i++) {
        array.push(binary.charCodeAt(i));
    }
    return new Blob([new Uint8Array(array)], {type: 'image/png'});
}

function captureImage(video) {

    var canvas = document.createElement("canvas");
    canvas.width= 640;
    canvas.height= 480;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width,
    canvas.height);
    var data_url = canvas.toDataURL();

    return data_url;
 };

function sendImage(ws, videoElement){


    var currentInstant = new Date().getTime();
    var lapse = (currentInstant - last_instant) / 1000;

    if(lapse > time_threshold && ws.readyState === ws.OPEN){
        last_instant = currentInstant;
        var data_url = captureImage(videoElement);
        var image_blob = dataURLtoBlob(data_url);
        console.log(image_blob);
        ws.send(image_blob);
    }
}

