const roomName = JSON.parse(document.getElementById('room-name').textContent);
const color = JSON.parse(document.getElementById('color').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
    + color
    + '/'
);

place_kums = function() {
    console.log("hello");
    var mydiv = document.getElementById('6');
    var mycontent = document.createElement('div');
    mycontent.setAttribute('class', 'kum');
    document.getElementById('6').appendChild(mycontent);
    place_kum = function(square, index, arr) {
        console.log("setting kums for" + index.toString());
        console.log(square);
        console.log(square.getAttribute('kum'));
        for (let i = 0; i < parseInt(square.getAttribute('kum')); i++) {
            var kum_obj = document.createElement('div');
            console.log(kum_obj);
            kum_obj.setAttribute('class', 'kum');
            square.appendChild(kum_obj);
        }
    };
    console.log(document.querySelectorAll('[class="square"]')[0])
    document.querySelectorAll('[class="square"]').forEach(place_kum);
}

place_kums();

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.color + ':' + data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};