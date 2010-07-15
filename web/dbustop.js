/**
 * dbustop web client Javascript library
 */

function remoteCommand(command) {
    var remoteCmdUrl = ''
    if (command == 'LIST') {
        remoteCmdUrl = 'list.json'
    }

    $.getJSON(remoteCmdUrl, function(data) {
        $('#busNameList').html
    });
}
