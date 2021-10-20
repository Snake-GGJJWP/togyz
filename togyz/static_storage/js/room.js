const roomName = JSON.parse(document.getElementById('room-name').textContent);
const color = JSON.parse(document.getElementById('color').textContent);
const username = JSON.parse(document.getElementById('username').textContent);
if (color == "white") {
    var board_ind = ['1','2','3','4','5','6','7','8','9'];
}
else if (color == "black") {
    var board_ind = ['10','11','12','13','14','15','16','17','18'];
}

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
);

const gameSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chatGame/'
    + roomName
);

function set_fields_onclick (field, arr_i, arr) {
    let index = field.getAttribute('name');
    if (board_ind.includes(index)) {
        field.onclick = function(e) {
            gameSocket.send(JSON.stringify({
                'msg_type': 'move',
                'startField': index
            }))
        };
    }
}

function set_kums(){
    for (let i = 1; i<=18; i++) {
        let field = document.getElementById("field"+i);
        field.setAttribute('kum', 9);
    }
}

function place_kums() {
    place_kum = function(square, index, arr) {
        square.textContent = '';
        let kum = square.getAttribute('kum');
        for (let i = 0; i < Math.min(9, parseInt(kum)); i++) {
            let img = document.createElement('img');
            let src = document.getElementById('sphere').getAttribute('src')
            img.setAttribute('src', src);
            var kum_obj = document.createElement('div');
            if (i == 0){
                kum_obj.setAttribute('class', 'kum-up');
            }
            kum_obj.appendChild(img);
            square.appendChild(kum_obj);
        };
        let i = square.getAttribute('name') 
        document.getElementById('counter'+i).innerHTML = kum; 
    };
    console.log(document.querySelectorAll('[class="square"]')[0])
    document.querySelectorAll('[class="square"]').forEach(place_kum);
}

function place_kum_test(i, kum) {
    let field = document.getElementById('field'+(i-1));
    field.setAttribute('kum', kum);
    field.textContent = '';
    for (let i = 0; i < Math.min(9, parseInt(kum)); i++) {
        let img = document.createElement('img');
        let src = document.getElementById('sphere').getAttribute('src')
        img.setAttribute('src', src);
        var kum_obj = document.createElement('div');
        if (i == 0){
            kum_obj.setAttribute('class', 'kum-up');
        }
        kum_obj.appendChild(img);
        field.appendChild(kum_obj);
    }
}

// ## MAIN PART ##
console.log(color);
console.log(board_ind);
if (color != 'spec') {
    document.querySelectorAll('[class="square"]').forEach(set_fields_onclick);
}
set_kums();
place_kums();

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data.msgType);
    if (data.msgType == 'message') {
        document.querySelector('#chat-log').value += (
            data.messageFrom
            + ':'
            + data.message
            + '\n'
        );
    }
    /*else if (data.msgType == 'move') {
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
        startField.setAttribute('kum', '0');
        let kumEnd = endField.getAttribute('kum')
        endField.setAttribute('kum', parseInt(kumStart) + parseInt(kumEnd));
        place_kums();
    }
    else if (data.msgType == 'opponent_joined') {
        console.log('GAME HAS BEEN STARTED')
        document.querySelectorAll('[class="square"]').forEach(set_fields_onclick);
    }*/
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

gameSocket.onmessage = function (e) {
    data = JSON.parse(e.data);
    if (data.msgType == 'opponent_joined') {
        console.log('GAME HAS BEEN STARTED');
    }
    else if (data.msgType == 'denied') {
        console.log(data.comment);
    }
    else if (data.msgType == 'move') {
        var position = data.current_position;
        for (var key in position) {
            place_kum_test(key, position[key])
        }
    }
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