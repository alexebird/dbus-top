/**
 * dbustop web client Javascript library.
 *
 * Author: Alex Bird
 * Created: July 22, 2010
 */

var canvas;
var ctx;
var clientList;

///////////////////// begin class Client /////////////////////
// Contsructor
function Client(name) {
    this.drawOnCanvas = false;
    this.name = name;
    jqElement = $("<div class='listItem'>" + this.name + "</div>");
    this.domElement = jqElement.get(0);
    jqElement.data('client', this);
    jqElement.click(function () {
        client = $(this).data('client');
        client.drawOnCanvas = ! client.drawOnCanvas;
        //alert(client.drawOnCanvas);
        clientList.update();
    });
    this.locationX = 10;
    this.locationY = 10;
    this.height = 60;
    ctx.font = "12pt sans-serif";
    this.nameWidth = Math.ceil(ctx.measureText(this.name).width);
    this.width = this.nameWidth + 40;
}

// Method
Client.prototype.draw = function () {
    if (this.drawOnCanvas == false)
        return;

    ctx.font = "12pt sans-serif";
    ctx.textBaseline = "middle";
    ctx.fillStyle = "rgb(255, 0, 0)";
    ctx.fillRect(this.locationX, this.locationY, this.width, this.height);
    ctx.fillStyle = "rgb(0, 0, 0)";
    ctx.fillText(this.name, this.locationX + 20, this.locationY + this.height / 2);
}
///////////////////// end class

///////////////////// begin class ClientList /////////////////////
// Contsructor
function ClientList() {
    this.clients = [];
}

// Method
ClientList.prototype.update = function () {
    //this.clients[80].drawOnCanvas = true; 
    clearCanvas();
    for (var i = 0; i < this.clients.length; i++) {
        c = this.clients[i]; 
        $(c.domElement).appendTo('#busNameList');
        c.draw();
    }
    //c = this.clients[80]; 
    //$(c.domElement).appendTo('#busNameList');
    //c.draw();
}

// Method
ClientList.prototype.add = function (client) {
    this.clients.push(client);
}

// Method
ClientList.prototype.clear = function () {
    this.clients = [];
}
///////////////////// end class

clientList = new ClientList;

function getRemoteBusNameList(bus) {
    $.getJSON('/ajax', {"cmd": "list", "bus": bus}, function(data, textStatus, XMLHttpRequest) {
        clientList.clear();
        for (var i = 0; i <  data.length; i++) {
            clientList.add(new Client(data[i]));
        }
        clientList.update();
    });
}

function getRemoteMessages() {
    $.getJSON('/ajax', {"cmd": "msg"}, function(data, textStatus, XMLHttpRequest) {
        //alert(data.length);
        //busNameList.names = data;
        //busNameList.update();
    });
}

/*function getRemotePing() {
    $.get('/ajax', {"cmd": "ping"}, function(data, textStatus, XMLHttpRequest) {
        alert(textStatus + ': ' + data);
    });
}*/

function initCanvas() {
    canvas = document.getElementById('canvas');
    if (canvas.getContext) {
        ctx = canvas.getContext('2d');
    }
}

function clearCanvas() {
    w = canvas.width;
    h = canvas.height;
    ctx.clearRect(0, 0, w, h);
}
