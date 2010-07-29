/**
 * dbustop web client Javascript library.
 *
 * Author: Alex Bird
 * Created: July 22, 2010
 */

var canvas;
var ctx;
var clientList;

// Create a point object from a set of coordinates.
function createPoint(x, y) {
    var o = new Object;
    o.x = x;
    o.y = y;
    return o;
}

///////////////////// begin class Client /////////////////////
// Contsructor
function Client(name) {
    this.drawOnCanvas = false;
    this.name = name;
    jqElement = $("<div class='listItem'><div class='clientName'>" + this.name + "</div><div class='addOrRemoveButton'>+</div></div>");
    this.domElement = jqElement.get(0);
    jqElement.data('client', this);
    jqElement.click(function () {
        client = $(this).data('client');  // get the Client object.
        client.drawOnCanvas = ! client.drawOnCanvas;
        var symbol = "+";
        if (client.drawOnCanvas) {
            symbol = "-";
        }
        $(client.domElement).find(".addOrRemoveButton").html(symbol);
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
Client.prototype.asPolygon = function () {
    var topLeft = createPoint(this.locationX, this.locationY);
    var topRight = createPoint(this.locationX + this.width, this.locationY);
    var bottomRight = createPoint(this.locationX + this.width, this.locationY + this.height);
    var bottomLeft = createPoint(this.locationX, this.locationY + this.height);
    return [topLeft, topRight, bottomRight, bottomLeft];
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
    ctx.fillText(this.name, this.locationX + 20, this.locationY + this.height / 2.0);
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

function translateEventCoords(e) {
    var offset = $(canvas).offset();
    var rv = new Object;
    rv.pageX = e.pageX - offset.left;
    rv.pageY = e.pageY - offset.top;
    return rv;
}

function initCanvas() {
    canvas = document.getElementById('canvas');
    if (canvas.getContext) {
        ctx = canvas.getContext('2d');
        resizeCanvas = function() {
            canvasPane = $('#canvasPane');
            canvas.setAttribute('width', canvasPane.width() - 2);
            canvas.setAttribute('height', canvasPane.height() - 2);
        }
        resizeCanvas();
        $(window).resize(resizeCanvas);

        $(canvas).mousemove(function (e) {
            var trans = translateEventCoords(e);
            $("#messageListPane").html("(" + trans.pageX + ", " + trans.pageY + ")");
        });

        $(canvas).mousedown(function (e) {
            var trans = translateEventCoords(e);
            $("#messageListPane").append("mousedown(" + trans.pageX + ", " + trans.pageY + ")");
        });
        $(canvas).mouseup(function (e) {
            var trans = translateEventCoords(e);
            $("#messageListPane").append("mouseup(" + trans.pageX + ", " + trans.pageY + ")");
        });
    }
}

function clearCanvas() {
    w = canvas.width;
    h = canvas.height;
    ctx.clearRect(0, 0, w, h);
}

//+ Jonas Raoni Soares Silva
//@ http://jsfromhell.com/math/is-point-in-poly [rev. #0]
//
//Checks whether the point is inside the polygon.
//
//polygon, array of points, each element must be an object with two properties (x and y)
//point, object with two properties (x and y)

function isPointInPoly(poly, pt){
    for(var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i)
      ((poly[i].y <= pt.y && pt.y < poly[j].y) || (poly[j].y <= pt.y && pt.y < poly[i].y))
      && (pt.x < (poly[j].x - poly[i].x) * (pt.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)
        && (c = !c);
    return c;
}
