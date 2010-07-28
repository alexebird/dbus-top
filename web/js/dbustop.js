/**
 * dbustop web client Javascript library.
 *
 * Author: Alex Bird
 * Created: July 22, 2010
 */


// being class BusNameList
// Contsructor
function BusNameList() {
    this.names = null;
}

// Method
BusNameList.prototype.update = function () {
    for (var i = 0; i <  this.names.length; i++) {
        $("<div class='listItem'>" + this.names[i] + "</div>").appendTo('#busNameList');
    }
}
// End class BusNameList

var busNameList = new BusNameList;

function getRemoteBusNameList(bus) {
    $.getJSON('/ajax', {"cmd": "list", "bus": bus}, function(data, textStatus, XMLHttpRequest) {
        busNameList.names = data;
        busNameList.update();
    });
}

/*function getRemotePing() {
    $.get('/ajax', {"cmd": "ping"}, function(data, textStatus, XMLHttpRequest) {
        alert(textStatus + ': ' + data);
    });
}*/

function draw() {
    var canvas = document.getElementById('canvas');
    if (canvas.getContext) {
        var ctx = canvas.getContext('2d');
        ctx.fillStyle = "rgb(200,0,0)";
        ctx.fillRect (10, 10, 55, 50);
        ctx.fillStyle = "rgba(0,200,0,0.5)";
        ctx.fillRect (20, 30, 550, 50);
    }
}
