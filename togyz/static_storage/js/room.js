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

function set_fields_onclick (field, arr_i, arr) {
    field.onclick = function(e) {
        if (parseInt(field.getAttribute('kum')) > 0) {
            let field_i = parseInt(field.getAttribute('name'));
            chatSocket.send(JSON.stringify({
                'msgType': "move",
                'message': color + "has made a move",
                'startField': field_i,
                'endField': Math.max(1, ((field_i + parseInt(field.getAttribute('kum'))) % 19)) 
            }))
        }
    };
};

function set_kums(){
    for (let i = 1; i<=9; i++) {
        let field = document.getElementById("field"+i)
        field.setAttribute('kum', 2)
    }
}

function place_kums() {
    console.log("hello");
    place_kum = function(square, index, arr) {
        console.log("setting kums for" + index.toString());
        console.log(square);
        console.log(square.getAttribute('kum'));
        square.textContent = '';
        for (let i = 0; i < parseInt(square.getAttribute('kum')); i++) {
            let kum_obj = document.createElement('div');
            console.log(kum_obj);
            kum_obj.setAttribute('class', 'kum');
            square.appendChild(kum_obj);
        };
    };
    console.log(document.querySelectorAll('[class="square"]')[0])
    document.querySelectorAll('[class="square"]').forEach(place_kum);
}

document.querySelectorAll('[class="square"]').forEach(set_fields_onclick);
set_kums();
place_kums();

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data.msgType);
    if (data.msgType == 'message') {
        document.querySelector('#chat-log').value += (
            data.color
            + ':'
            + data.message
            + '\n'
        );
    }
    else if (data.msgType == 'move') {
        document.querySelector('#chat-log').value += (
            '[MOVE] '
            + data.color
            + ' moved from '
            + data.startField
            + ' to '
            + data.endField
            + '\n'
        );
        let startField = document.getElementById('field' + data.startField.toString());
        let endField = document.getElementById('field' + data.endField.toString());
        let kumStart = startField.getAttribute('kum');
        let kumEnd = endField.getAttribute('kum')
        startField.setAttribute('kum', '0');
        endField.setAttribute('kum', parseInt(kumStart) + parseInt(kumEnd));
        place_kums();
    }
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
        'msgType': 'message',
        'message': message
    }));
    messageInputDom.value = '';
};