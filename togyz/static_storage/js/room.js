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
        document.getElementById('counter_'+i).innerHTML = kum; 
    };
    console.log(document.querySelectorAll('[class="square"]')[0])
    document.querySelectorAll('[class="square"]').forEach(place_kum);
}

function place_kum_test(index, kum) {
    if (index == 'white_pool' || index == 'black_pool') {
        var field = document.getElementById(index);
        field.textContent = '';
        for (let i = 0; i < Math.min(39, kum); i++) {
            let img = document.createElement('img');
            let src = document.getElementById('sphere').getAttribute('src');
            img.src = src;
            img.setAttribute('class',  (i % 2 == 0) ? 'up-pool' : 'bottom-pool');
            field.appendChild(img);
        }
    }
    else {
        let field = document.getElementById('field'+index);
        field.setAttribute('kum', kum);
        field.textContent = '';
        for (let i = 0; i < Math.min(12, parseInt(kum)); i++) {
            let img = document.createElement('img');
            let src = document.getElementById('sphere').getAttribute('src');
            img.src = src;
            let kum_obj = document.createElement('div');
            kum_obj.setAttribute('class', (i == 0) ? 'kum-up' : '');
            kum_obj.appendChild(img);
            field.appendChild(kum_obj);
        }
    }
    console.log(index)
    document.getElementById('counter_'+index).innerHTML = kum; 
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
            place_kum_test(key, position[key]);
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