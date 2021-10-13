document.querySelector('#room-name-input').focus();
document.querySelector('#room-name-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#room-name-submit').click();
    }
};

document.querySelector('#room-name-submit').onclick = function(e) {
    console.log(document.querySelector('#white').checked);
    if (document.querySelector('#white').checked) {
        var color = 'white';
    }
    else if (document.querySelector('#black').checked){
        var color = 'black';
    }
    console.log(color)
    var roomName = document.querySelector('#room-name-input').value;
    window.location.pathname = '/chat/' + roomName + '/' + color + '/';
};