/**
 * dbustop web client Javascript library.
 *
 * Author: Alex Bird
 * Created: July 22, 2010
 */

function remoteCommand(command) {
    var remoteCmdUrl = ''
        if (command == 'LIST') {
            remoteCmdUrl = '/dbustop?cmd=list&bus=session'
        }

    $.getJSON(remoteCmdUrl, function(data) {
            $('#busNameList').html
            });
}

function draw() {
    var canvas = document.getElementById('canvas');
    if (canvas.getContext) {
        var ctx = canvas.getContext('2d');
        ctx.fillStyle = "rgb(200,0,0)";
        ctx.fillRect (10, 10, 55, 50);
        ctx.fillStyle = "rgba(0,200,0,0.5)";
        ctx.fillRect (20, 10, 550, 50);
    }
}

