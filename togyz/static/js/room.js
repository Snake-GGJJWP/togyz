const roomName = JSON.parse(document.getElementById('room-name').textContent);
const color = JSON.parse(document.getElementById('color').textContent);
const username = JSON.parse(document.getElementById('username').textContent);

const colorOppose = {
    'white': 'black',
    'black': 'white'
};
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
    if (kum == 'X') {
        var sphere = 'red-sphere';
        kum = 1;
        document.getElementById('counter_'+index).innerHTML = 0;
    }
    else {
        var sphere = 'sphere';
        document.getElementById('counter_'+index).innerHTML = kum;
    }
    if (index == 'white_pool' || index == 'black_pool') {
        var field = document.getElementById(index);
        field.textContent = '';
        for (let i = 0; i < Math.min(27, kum); i++) {
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
            let src = document.getElementById(sphere).getAttribute('src');
            img.src = src;
            let kum_obj = document.createElement('div');
            kum_obj.setAttribute('class', (i == 0) ? 'kum-up' : '');
            kum_obj.appendChild(img);
            field.appendChild(kum_obj);
        }
    }
    console.log(index) 
}

// ## MAIN PART ##
console.log(color);
console.log(board_ind);
if (color != 'spec') {
    document.querySelectorAll('[class="square"]').forEach(set_fields_onclick);
}
// set_kums();
// place_kums();

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

function put_colors_on_usernames(data) {
    if (!data.is_started) {
        document.getElementById('white-player').style['color'] = 'black';
        document.getElementById('black-player').style['color'] = 'black';
    }
    else if (!data.is_finished){
        document.getElementById(data.color_turn+'-player').style['color'] = 'green';
        document.getElementById(colorOppose[data.color_turn]+'-player').style['color'] = 'red';
    }
}

function on_connect(data) {
    user_joined({
        username: data.player_white,
        color: 'white',
    });
    user_joined({
        username: data.player_black,
        color: 'black',
    });
    move({
        current_position: data.current_position,
        winner: data.winner,
        color_turn: data.color_turn,
        is_started: data.is_started,
        winner_color: data.winner_color
    });
}

function user_joined(data) {
    if (data.username) {
        document.getElementById('chat-log').value += (
            '[ACTION]: ' 
            + data.username
            + ' has just joined the room!'
            + '\n'
        );
    }
    if (data.color != 'spec') {
        document.getElementById(data.color + '-player').textContent = data.username;
    }
    if (data.is_started) {
        console.log('GAME HAS BEEN STARTED');
    }
    put_colors_on_usernames({
        'is_started': data.is_started,
        'color_turn': data.color_turn
    });
}

function denied(data) {
    console.log(data.comment);
}

function move(data) {
    var position = data.current_position;
    for (var key in position) {
        place_kum_test(key, position[key]);
    }
    if (data.winner) {
        console.log(data.winner + " WON");
        console.log(data.winner_color);
        document.getElementById(data.winner_color + '-player').style['color'] = 'gold';
        document.getElementById(colorOppose[data.winner_color]+ '-player').style['color'] = 'black';
        return
    }
    document.getElementById(data.color_turn+'-player').style['color'] = 'green';
    document.getElementById(colorOppose[data.color_turn]+'-player').style['color'] = 'red';
}

const onmessageFunctionsBank = {
    'on_connect': on_connect,
    'user_joined': user_joined,
    'denied': denied,
    'move': move
} 

gameSocket.onmessage = function (e) {
    data = JSON.parse(e.data);
    onmessageFunctionsBank[data.msgType](data);
    /*if (data.msgType == 'on_connect') {
        var position = data.current_position;
        for (var key in position) {
            place_kum_test(key, position[key]);
        }
        document.getElementById()
    }
    if (data.msgType == 'user_joined') {
        document.getElementById('chat-log').value = (
            '[ACTION]: ' 
            + data.username
            + ' has just joined the room!'
        );
        if (data.color != 'spec') {
            document.getElementById(data.color + '-player').textContent = data.username;
        }
        if (data.is_started) {
            console.log('GAME HAS BEEN STARTED');
        }
    }
    else if (data.msgType == 'denied') {
        console.log(data.comment);
    }
    else if (data.msgType == 'move') {
        var position = data.current_position;
        for (var key in position) {
            place_kum_test(key, position[key]);
        }
        if (data.winner) {
            console.log(data.winner + " WON")
        }
    }*/
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