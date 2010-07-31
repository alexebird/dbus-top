/**
 * dbustop web client Javascript library.
 *
 * Author: Alex Bird
 * Created: July 22, 2010
 */

// The main objects representing the UI.
var g_canvas;
var g_clientList;
var g_messageList;

/**
 * Initialize the UI.
 */
function init() {
    g_canvas = new CanvasClass;
    g_canvas.resizeCanvasToWindow();
    g_clientList = new DivList('busNameList');
    g_messageList = new DivList('messageList');

    $("#updateMessages").click(function () {
        getRemoteMessages();
    });
}

/**
 * Create a point object from a set of coordinates.
 */
function createPoint(x, y) {
    var o = new Object;
    o.x = x;
    o.y = y;
    return o;
}

function getRemoteBusNameList(bus) {
    $.getJSON('/ajax', {"cmd": "list", "bus": bus}, function(data, textStatus, XMLHttpRequest) {
        g_clientList.clear();
        for (var i = 0; i <  data.length; i++) {
            g_clientList.add(new Client(data[i]));
        }
    });
}

function getRemoteMessages() {
    $.getJSON('/ajax', {"cmd": "msg"}, function(data, textStatus, XMLHttpRequest) {
        //alert(data.length);
        for (var i = 0; i <  data.length; i++) {
            g_messageList.add(new DbusMessage(data[i]));
        }
    });
}

/*function getRemotePing() {
    $.get('/ajax', {"cmd": "ping"}, function(data, textStatus, XMLHttpRequest) {
        alert(textStatus + ': ' + data);
    });
}*/

/**
 * + Jonas Raoni Soares Silva
 * @ http://jsfromhell.com/math/is-point-in-poly [rev. #0]
 * 
 * Checks whether the point is inside the polygon.
 * 
 * polygon, array of points, each element must be an object with two properties (x and y)
 * point, object with two properties (x and y)
 */
function isPointInPoly(poly, pt){
    for(var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i)
        ((poly[i].y <= pt.y && pt.y < poly[j].y) || (poly[j].y <= pt.y && pt.y < poly[i].y))
          && (pt.x < (poly[j].x - poly[i].x) * (pt.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)
          && (c = !c);
    return c;
}

/*******************************************************************************
 * begin class DbusMessage
 */
// Contsructor
function DbusMessage(jsonMsg) {
    this.message_type = jsonMsg['message_type'];
    this.timestamp = jsonMsg['timestamp'];
    this.serial = jsonMsg['serial'];

    var html = "<div class='divListItem'>";
    html += "<div class='message'>" + this.message_type + ", ";
    html += this.serial;
    html += "</div>";
    jqElement = $(html);
    this.domElement = jqElement.get(0);
    jqElement.data('message', this);
}

DbusMessage.prototype.buildSignal = function(jsonMsg) {
    this.objectPath = jsonMsg['object'];
    this.interface = jsonMsg['interface'];
    this.member = jsonMsg['member'];
}

DbusMessage.prototype.buildMethodCall = function(jsonMsg) {
    this.sender = jsonMsg['sender'];
    this.objectPath = jsonMsg['object'];
    this.interface = jsonMsg['interface'];
    this.member = jsonMsg['member'];
}

DbusMessage.prototype.buildMethodReturn = function(jsonMsg) {
    this.replySerial= jsonMsg['reply_serial'];
    this.destination = jsonMsg['destination'];
}

DbusMessage.prototype.buildError = function(jsonMsg) {
    this.replySerial= jsonMsg['reply_serial'];
    this.destination = jsonMsg['destination'];
}
/* end Class */

/*******************************************************************************
 * begin class Client
 */
// Contsructor
function Client(name) {
    this.drawOnCanvas = false;
    this.name = name;
    var html = "<div class='divListItem'>";
    html += "<div class='clientName'>" + this.name + "</div>";
    html += "<div class='addOrRemoveButton'>+</div></div>";
    jqElement = $(html);
    this.domElement = jqElement.get(0);
    jqElement.data('client', this);
    jqElement.click(function () {
        client = $(this).data('client');  // get the Client object.
        client.drawOnCanvas = !client.drawOnCanvas;
        var symbol;
        if (client.drawOnCanvas) {
            symbol = "-";
            g_canvas.addDrawnObject(client);
            $(client.domElement).find(".addOrRemoveButton").addClass("removeMinusSign");
        }
        else {
            var symbol = "+";
            g_canvas.removeDrawnObject(client);
            $(client.domElement).find(".addOrRemoveButton").removeClass("removeMinusSign");
        }
        $(client.domElement).find(".addOrRemoveButton").html(symbol);
        g_canvas.draw();
    });
    this.locationX = 10;
    this.locationY = 10;
    this.height = 60;
    g_canvas.context.font = "12pt sans-serif";
    this.nameWidth = Math.ceil(g_canvas.context.measureText(this.name).width);
    this.width = this.nameWidth + 40;
    this.zOrder = -1;
    this.drawingOptions = new Object;
    this.drawingOptions.font = "12pt sans-serif";
    this.drawingOptions.textBaseline = "middle";
    this.drawingOptions.rectFillStyle = "rgb(255, 0, 0)";
    this.drawingOptions.textFillStyle = "rgb(0, 0, 0)";
}

Client.prototype.asPolygon = function () {
    var topLeft = createPoint(this.locationX, this.locationY);
    var topRight = createPoint(this.locationX + this.width, this.locationY);
    var bottomRight = createPoint(this.locationX + this.width, this.locationY + this.height);
    var bottomLeft = createPoint(this.locationX, this.locationY + this.height);
    return [topLeft, topRight, bottomRight, bottomLeft];
}

/**
 * e - the event
 * point - the translated point on the canvas.
 */
Client.prototype.dragStarted = function (point) {
    this.drawingOptions.rectFillStyle = "rgb(0, 255, 0)";
    var dragAnchor = createPoint(point.x - this.locationX, point.y - this.locationY);
    return dragAnchor;
}

/**
 * e - the event
 * point - the translated point on the canvas.
 */
Client.prototype.dragEnded = function () {
    this.drawingOptions.rectFillStyle = "rgb(255, 0, 0)";
}

/**
 * e - the event
 * point - the translated point on the canvas.
 */
Client.prototype.dragging = function (point) {
    this.locationX = point.x;
    this.locationY = point.y;
}

Client.prototype.draw = function (context) {
    if (this.drawOnCanvas == false)
        return;

    context.font = this.drawingOptions.font;
    context.textBaseline = this.drawingOptions.textBaseline;
    context.fillStyle = this.drawingOptions.rectFillStyle;
    context.fillRect(this.locationX, this.locationY, this.width, this.height);
    context.fillStyle = this.drawingOptions.textFillStyle;
    context.fillText(this.name, this.locationX + 20, this.locationY + this.height / 2.0);
}
/* end Class */

/*******************************************************************************
 * begin class DivList
 *
 * Maintains an HTML div that is a list UI element.
 */
// Contsructor
function DivList(divId) {
    this.items = [];
    this.jqDivListDivId = $('#' + divId);
    this.jqDivListDivId.addClass('divList');
}

DivList.prototype.add = function (item) {
    this.items.push(item);
    $(item.domElement).appendTo(this.jqDivListDivId);
}

DivList.prototype.clear = function () {
    this.items = [];
    $(this.jqDivListDivId).empty();
}
/* end Class */

/*******************************************************************************
 * begin class CanvasClass
 */
// Contsructor
function CanvasClass() {
    this.canvas = document.getElementById('canvas');
    this.context = this.canvas.getContext('2d');
    this.dragAndDrop = new DragAndDrop;
    this.drawnObjects = [];
    this.currentZOrder = 0;

    $(window).resize(this.resizeCanvasToWindow);
    $(this.canvas).bind('mousemove mousedown mouseup', function (e) {
        g_canvas.handleEvent(e);
    });
}

CanvasClass.prototype.handleEvent = function (e) {
    var point = this.translateEventCoords(e);
    $("#log").html(e.type + "(" + point.x + ", " + point.y + ")");

    if (e.type == 'mousedown') {
        var obj = this.getDrawnObjectAtPoint(point);
        if (obj) {
            this.dragAndDrop.startDrag(obj, point);
        }
    }
    else if (e.type == 'mouseup') {
        this.dragAndDrop.endDrag(point);
    }
    else if (e.type == 'mousemove') {
        this.dragAndDrop.dragTo(point);
    }

    this.draw();
}

CanvasClass.prototype.getDrawnObjectAtPoint = function(point) {
    // Iterate in reverse so that objects with a higher Z-order are checked first.
    for (var i = this.drawnObjects.length - 1; i >= 0 ; i--) {
        var obj = this.drawnObjects[i];
        if (isPointInPoly(obj.asPolygon(), point)) {
            return obj;
        }
    }
    return null;
}

CanvasClass.prototype.resizeCanvasToWindow = function() {
    var canvasPane = $('#canvasPane');
    g_canvas.canvas.setAttribute('width', canvasPane.width() - 2);
    g_canvas.canvas.setAttribute('height', canvasPane.height() - 2);
    g_canvas.draw();
}

CanvasClass.prototype.clearCanvas = function () {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    this.currentZOrder = 0;
}

CanvasClass.prototype.addDrawnObject = function (obj) {
    obj.zOrder = this.currentZOrder++;
    this.drawnObjects.push(obj);
}

CanvasClass.prototype.removeDrawnObject = function (obj) {
    var i;
    for (i = 0; i < this.drawnObjects.length; i++) {
        var e = this.drawnObjects[i];
        if (e == obj) {
            break;
        }
    }
    this.drawnObjects.splice(i, 1);  // Remove the object.
}

CanvasClass.prototype.draw = function () {
    this.clearCanvas();
    for (var i = 0; i < this.drawnObjects.length; i++) {
        var e = this.drawnObjects[i];
        e.draw(this.context);
    }
}

CanvasClass.prototype.translateEventCoords = function (e) {
    var offset = $(this.canvas).offset();
    var rv = new Object;
    rv.x = e.pageX - offset.left;
    rv.y = e.pageY - offset.top;
    return rv;
}
/* end Class */

/*******************************************************************************
 * begin class DragAndDrop
 */
// Contsructor
function DragAndDrop() {
    this.draggingObject = null;
    this.dragAnchorOffset = null;
}

DragAndDrop.prototype.startDrag = function (obj, point) {
    this.draggingObject = obj;
    this.dragAnchorOffset = obj.dragStarted(point);
}

DragAndDrop.prototype.dragTo = function (point) {
    if (this.draggingObject) {
        // Change the drag point so that the user's cursor stays at the same place relative to the object.
        this.draggingObject.dragging(createPoint(point.x - this.dragAnchorOffset.x, point.y - this.dragAnchorOffset.y));
    }
}

DragAndDrop.prototype.endDrag = function (point) {
    if (this.draggingObject) {
        this.draggingObject.dragEnded();
        this.draggingObject = null;
        this.dragAnchorOffset = null;
    }
}
/* end Class */
